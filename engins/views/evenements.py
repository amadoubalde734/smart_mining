from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from engins.models import EvenementEngin
from personnel.models import Employe
from engins.forms import EvenementEnginForm
from documents.forms import FichierJointForm

# ===============================
# LISTE DES EVENEMENTS
# ===============================
@login_required
def evenement_list(request):
    evenements = EvenementEngin.objects.select_related(
        'engin', 'type_evenement', 'statut_camion', 'statut_radar', 'responsable_saisie', 'valideur'
    ).all().order_by('-date_debut')

    context = {
        'evenements': evenements,
        'total_evenements': evenements.count(),
        'upcoming_events': evenements.filter(date_debut__gte=timezone.now().date()).count(),
        'past_events': evenements.filter(date_fin__lt=timezone.now().date()).count(),
    }
    return render(request, 'backend/pages/engins/evenements/evenement_list.html', context)

# ===============================
# AJOUT D'UN EVENEMENT
# ===============================
@login_required
def evenement_create(request):
    if request.method == "POST":
        form = EvenementEnginForm(request.POST)
        document_form = FichierJointForm(
            request.POST,
            request.FILES,
            module="EvenementEngin"
        )

        if form.is_valid() and document_form.is_valid():
            evenement = form.save(commit=False)
            evenement.responsable_saisie = Employe.objects.get(user=request.user)
            evenement.save()

            # Sauvegarde document (si présent)
            if document_form.cleaned_data.get("fichier"):
                document = document_form.save(commit=False)
                document.content_object = evenement
                document.save()

            messages.success(request, "Événement créé avec succès !")
            return redirect("engins:evenement_list")

        messages.error(request, "Veuillez corriger les erreurs du formulaire.")

    else:
        form = EvenementEnginForm()
        document_form = FichierJointForm(module="EvenementEngin")

    return render(
        request,
        "backend/pages/engins/evenements/evenement_form.html",
        {
            "form": form,
            "document_form": document_form
        }
    )
# ===============================
# MODIFICATION D'UN EVENEMENT
# ===============================
@login_required
def evenement_update(request, slug):
    evenement = get_object_or_404(EvenementEngin, slug=slug)

    if request.method == "POST":
        form = EvenementEnginForm(request.POST, instance=evenement)
        document_form = FichierJointForm(
            request.POST,
            request.FILES,
            module="EvenementEngin"
        )

        if form.is_valid() and document_form.is_valid():
            form.save()

            if document_form.cleaned_data.get("fichier"):
                document = document_form.save(commit=False)
                document.content_object = evenement
                document.save()

            messages.success(request, "Événement modifié avec succès !")
            return redirect("engins:evenement_list")

        messages.error(request, "Veuillez corriger les erreurs du formulaire.")

    else:
        form = EvenementEnginForm(instance=evenement)
        document_form = FichierJointForm(module="EvenementEngin")

    return render(
        request,
        "backend/pages/engins/evenements/evenement_form.html",
        {
            "form": form,
            "document_form": document_form,
            "modifier": True,
            "evenement": evenement
        }
    )

# ===============================
# SUPPRESSION D'UN EVENEMENT
# ===============================
@login_required
def evenement_delete(request, slug):
    evenement = get_object_or_404(EvenementEngin, slug=slug)
    if request.method == "POST":
        evenement.delete()
        messages.success(request, "Événement supprimé avec succès !")
        return redirect('engins:evenement_list')

    return render(request, 'backend/pages/engins/evenements/confirm_delete.html', {'obj': evenement})

# ===============================
# DETAIL D'UN EVENEMENT
# ===============================
@login_required
def evenement_detail(request, slug):
    evenement = get_object_or_404(EvenementEngin, slug=slug)
    context = {
        'evenement': evenement,
        'pieces_jointes': evenement.pieces_jointes.all()
    }
    return render(request, 'backend/pages/engins/evenements/evenement_detail.html', context)
