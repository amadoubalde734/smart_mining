from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views import View
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.core.mail import EmailMessage, send_mail, get_connection
import json
import random
from datetime import timedelta

from accounts.models import CustomUser
from .forms import CustomPasswordChangeForm, RequestResetCodeForm, ResetPasswordWithCodeForm
from .utils import account_activation_token
from parametrage.models import Societe, Ville, Site, EmailSettings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site



# -----------------------------------------
# Validation
# -----------------------------------------

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email invalide'}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email déjà utilisé'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Utilisez uniquement des caractères alphanumériques'}, status=400)
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Nom d’utilisateur déjà utilisé'}, status=409)
        return JsonResponse({'username_valid': True})


# -----------------------------------------
# Inscription
# -----------------------------------------

class RegistrationView(View):
    def get_template_name(self, request):
        return 'front/authentification_front/register_front.html' if 'front' in request.path else 'admin/authentification/register.html'

    def get(self, request):
        return render(request, self.get_template_name(request))

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next', 'index')

        context = {'fieldValues': request.POST}
        template_name = self.get_template_name(request)

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Nom d’utilisateur déjà utilisé.')
            return render(request, template_name, context)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email déjà utilisé.')
            return render(request, template_name, context)

        if len(password) < 6:
            messages.error(request, 'Le mot de passe est trop court.')
            return render(request, template_name, context)

        user = CustomUser.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = get_current_site(request).domain
        link = reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': token})
        activate_url = f'http://{domain}{link}?next={next_url}'

        email_subject = 'Activez votre compte'
        email_body = f'Bonjour {user.username},\n\nVeuillez activer votre compte :\n{activate_url}'
        EmailMessage(email_subject, email_body, 'noreply@monsite.com', [email]).send()

        messages.success(request, 'Compte créé. Vérifiez votre email.')
        return render(request, template_name)


# -----------------------------------------
# Activation
# -----------------------------------------

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if user.is_active:
                return redirect('accounts:admin_login')

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Compte activé.')
                return redirect('accounts:admin_login')
        except Exception:
            pass

        messages.error(request, 'Lien invalide ou expiré.')
        return redirect('accounts:admin_login')


# -----------------------------------------
# Connexion admin
# -----------------------------------------

class AdminLoginView(View):
    template_name = 'backend/authentification/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} 👋')
            return redirect('/dashboard/')

        messages.error(request, '⚠️ Identifiants invalides ou compte inactif.')
        return render(request, self.template_name)


# -----------------------------------------
# Connexion front
# -----------------------------------------

class FrontLoginView(View):
    def get(self, request):
        return render(request, 'front/authentification_front/login_front.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect('/portail/')
        messages.error(request, 'Identifiants invalides ou compte inactif.')
        return render(request, 'front/authentification_front/login_front.html')


# -----------------------------------------
# Déconnexion
# -----------------------------------------

class LogoutView(View):
    def post(self, request):
        auth_logout(request)
        messages.success(request, 'Déconnecté avec succès.')
        if 'admin' in request.path:
            return redirect('accounts:admin_login')
        else:
            return redirect('accounts:front_login')


# -----------------------------------------
# Ajout et modification utilisateur (Admin)
# -----------------------------------------

class AddUserView(View):
    def get(self, request):
        societes = Societe.objects.all()
        villes = Ville.objects.all()
        sites = Site.objects.all()
        role_choices = CustomUser.ROLE_CHOICES

        return render(request, 'backend/authentification/add_user.html', {
            'societes': societes,
            'villes': villes,
            'sites': sites,
            'role_choices': role_choices,
        })

    def post(self, request):
        nom = request.POST.get('nom', '').strip()
        login_name = request.POST.get('login', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        ville_id = request.POST.get('ville')
        site_id = request.POST.get('site')
        societe_id = request.POST.get('societe')
        contact = request.POST.get('contact', '').strip()
        role = request.POST.get('role')
        image = request.FILES.get('image')

        if CustomUser.objects.filter(username=login_name).exists():
            messages.error(request, "Login déjà utilisé.")
            return redirect('accounts:add_user')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return redirect('accounts:add_user')

        if len(password) < 6:
            messages.error(request, "Mot de passe trop court.")
            return redirect('accounts:add_user')

        if role not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:
            messages.error(request, "Rôle sélectionné invalide.")
            return redirect('accounts:add_user')

        # Découpage du nom
        first_name, last_name = '', ''
        if nom:
            parts = nom.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

        # Création utilisateur
        user = CustomUser(
            username=login_name,
            email=email,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            role=role,
            ville_id=ville_id or None,
            site_id=site_id or None,
            id_societe_id=societe_id or None,
        )
        user.set_password(password)
        if image:
            user.avatar = image
        user.save()

        messages.success(request, "Utilisateur créé avec succès.")
        return redirect('accounts:add_user')


class EditUserView(View):
    def get(self, request, user_id):
        user_instance = get_object_or_404(CustomUser, pk=user_id)
        societes = Societe.objects.all()
        villes = Ville.objects.all()
        sites = Site.objects.all()
        role_choices = CustomUser.ROLE_CHOICES

        return render(request, 'backend/authentification/add_user.html', {
            'user_instance': user_instance,
            'societes': societes,
            'villes': villes,
            'sites': sites,
            'role_choices': role_choices,
        })

    def post(self, request, user_id):
        user_instance = get_object_or_404(CustomUser, pk=user_id)
        nom = request.POST.get('nom', '').strip()
        login_name = request.POST.get('login', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        ville_id = request.POST.get('ville')
        site_id = request.POST.get('site')
        societe_id = request.POST.get('societe')
        contact = request.POST.get('contact', '').strip()
        role = request.POST.get('role')
        image = request.FILES.get('image')

        if CustomUser.objects.exclude(pk=user_instance.id).filter(username=login_name).exists():
            messages.error(request, "Login déjà utilisé.")
            return redirect('accounts:edit_user', user_id=user_id)

        if CustomUser.objects.exclude(pk=user_instance.id).filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return redirect('accounts:edit_user', user_id=user_id)

        if role not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:
            messages.error(request, "Rôle sélectionné invalide.")
            return redirect('accounts:edit_user', user_id=user_id)

        first_name, last_name = '', ''
        if nom:
            parts = nom.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

        # Mise à jour
        user_instance.username = login_name
        user_instance.email = email
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.contact = contact
        user_instance.role = role
        user_instance.ville_id = ville_id or None
        user_instance.site_id = site_id or None
        user_instance.id_societe_id = societe_id or None
        if password:
            user_instance.set_password(password)
        if image:
            user_instance.avatar = image
        user_instance.save()

        messages.success(request, "Utilisateur modifié avec succès.")
        return redirect('accounts:list_users')


# -----------------------------------------
# Liste et suppression des utilisateurs
# -----------------------------------------

class ListUsersView(LoginRequiredMixin, View):
    template_name = 'backend/authentification/list_users.html'

    def get(self, request):
        search = request.GET.get('q', '')
        queryset = CustomUser.objects.select_related('ville', 'site', 'id_societe')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            )
        return render(request, self.template_name, {'users': queryset})


class DeleteUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        if request.user.role != 'administrateur':
            messages.error(request, "Accès refusé.")
            return redirect('accounts:list_users')

        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect('accounts:list_users')


# -----------------------------------------
# Changement de mot de passe (admin)
# -----------------------------------------

class ChangeUserPasswordView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'backend/authentification/change_password.html'

    def test_func(self):
        return self.request.user.role == 'administrateur'

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        form = CustomPasswordChangeForm(user=user)
        return render(request, self.template_name, {'form': form, 'user_target': user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        form = CustomPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Mot de passe modifié pour {user.get_full_name()}.")
            return redirect('accounts:list_users')
        messages.error(request, "Veuillez corriger les erreurs.")
        return render(request, self.template_name, {'form': form, 'user_target': user})


# -----------------------------------------
# Utilisateurs connectés
# -----------------------------------------

class ConnectedUsersView(LoginRequiredMixin, View):
    template_name = 'backend/authentification/connected_users.html'

    def get(self, request):
        sessions = Session.objects.filter(expire_date__gte=now())
        user_ids = [s.get_decoded().get('_auth_user_id') for s in sessions if s.get_decoded().get('_auth_user_id')]
        users = CustomUser.objects.filter(id__in=user_ids).select_related('ville', 'site', 'id_societe')
        return render(request, self.template_name, {'users': users})


# -----------------------------------------
# Réinitialisation de mot de passe avec code
# -----------------------------------------

class ResetCodeView(View):
    template_name_request = 'backend/authentification/reset_request.html'
    template_name_reset = 'backend/authentification/reset_password.html'
    code_validity_minutes = 15

    def get(self, request):
        form = RequestResetCodeForm()
        return render(request, self.template_name_request, {'form': form})

    def post(self, request):
        form = RequestResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "Utilisateur non trouvé.")
                return render(request, self.template_name_request, {'form': form})

            code = str(random.randint(100000, 999999))
            user.reset_code = code
            user.reset_code_expiry = now() + timedelta(minutes=self.code_validity_minutes)
            user.save()

            try:
                email_config = EmailSettings.objects.first()
                connection = get_connection(
                    backend=email_config.email_backend,
                    host=email_config.email_host,
                    port=email_config.email_port,
                    username=email_config.email_host_user,
                    password=email_config.email_host_password,
                    use_tls=email_config.email_use_tls,
                )
                send_mail(
                    subject="Code de réinitialisation QSE360",
                    message=f"Bonjour {user.username},\n\nVoici votre code de réinitialisation valable {self.code_validity_minutes} minutes : {code}\n\nMerci.",
                    from_email=email_config.default_from_email,
                    recipient_list=[user.email],
                    connection=connection,
                    fail_silently=False,
                )
                messages.success(request, f"Code de réinitialisation envoyé à {user.email}.")
            except Exception as e:
                messages.error(request, f"Impossible d'envoyer l'email: {e}")

            return redirect('accounts:reset_code_verify', user_id=user.id)
        return render(request, self.template_name_request, {'form': form})


class ResetPasswordWithCodeView(View):
    template_name = 'backend/authentification/reset_password.html'

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = ResetPasswordWithCodeForm(user=user)
        return render(request, self.template_name, {'form': form, 'user_target': user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = ResetPasswordWithCodeForm(user=user, data=request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code != user.reset_code:
                messages.error(request, "Code incorrect.")
                return render(request, self.template_name, {'form': form, 'user_target': user})
            form.save()
            user.reset_code = None
            user.save()
            messages.success(request, "Mot de passe réinitialisé avec succès.")
            return redirect('accounts:admin_login')
        return render(request, self.template_name, {'form': form, 'user_target': user})
