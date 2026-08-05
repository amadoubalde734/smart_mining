from django.shortcuts import render

# Create your views here.
# ==========================================
# Imports
# ==========================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
import secrets

# Forms et modèles
from .forms import SocieteForm, VilleForm, SiteForm, DepartementForm, ServiceForm, FonctionForm
from .models import Societe, Ville, Site, Departement, Service, Fonction
from personnel.models import Ville as PersonnelVille, Site as PersonnelSite  # Si utilisé ailleurs


# ==========================================
# SOCIÉTÉS
# ==========================================
@login_required
def ajouter_societe(request):
    """Ajouter une nouvelle société"""
    form = SocieteForm()
    if request.method == "POST":
        form = SocieteForm(request.POST)
        if form.is_valid():
            libelle = form.cleaned_data['libelle'].strip()
            if Societe.objects.filter(libelle__iexact=libelle).exists():
                messages.error(request, f"La société '{libelle}' existe déjà.")
            else:
                instance = form.save(commit=False)
                instance.slug = slugify(libelle) + '-' + secrets.token_urlsafe(8)
                instance.save()
                messages.success(request, f"La société '{libelle}' a été ajoutée avec succès !")
                return redirect('parametrage:liste_societes')
    societes = Societe.objects.all()
    return render(request, 'backend/pages/parametrage/liste_societes.html', {
        'societes': societes,
        'form': form,
        'modifier': False,
    })


@login_required
def modifier_societe(request, pk):
    """Modifier une société existante"""
    societe = get_object_or_404(Societe, pk=pk)
    if request.method == "POST":
        form = SocieteForm(request.POST, instance=societe)
        if form.is_valid():
            libelle = form.cleaned_data['libelle'].strip()
            if Societe.objects.filter(libelle__iexact=libelle).exclude(pk=pk).exists():
                messages.error(request, f"La société '{libelle}' existe déjà.")
            else:
                instance = form.save(commit=False)
                instance.slug = slugify(libelle) + '-' + secrets.token_urlsafe(8)
                instance.save()
                messages.success(request, f"La société '{libelle}' a été modifiée avec succès !")
                return redirect('parametrage:liste_societes')
    else:
        form = SocieteForm(instance=societe)
    societes = Societe.objects.all()
    return render(request, 'backend/pages/parametrage/liste_societes.html', {
        'societes': societes,
        'form': form,
        'modifier': True,
    })


@login_required
def supprimer_societe(request, pk):
    """Supprimer une société"""
    societe = get_object_or_404(Societe, pk=pk)
    societe.delete()
    messages.success(request, "La société a été supprimée.")
    return redirect('parametrage:liste_societes')


@login_required
def liste_societes(request):
    """Lister toutes les sociétés"""
    societes = Societe.objects.all()
    form = SocieteForm()
    return render(request, 'backend/pages/parametrage/liste_societes.html', {
        'societes': societes,
        'form': form,
        'modifier': False,
    })


# ==========================================
# VILLES
# ==========================================
@login_required
def ajouter_ville(request):
    """Ajouter une ville"""
    form = VilleForm()
    villes = Ville.objects.all()
    if request.method == "POST":
        form = VilleForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.libelle) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "La ville a été ajoutée avec succès !")
            return redirect('parametrage:ajouter_ville')
    return render(request, 'backend/pages/parametrage/liste_villes.html', {
        'form': form,
        'villes': villes,
        'modifier': False,
    })


@login_required
def modifier_ville(request, pk):
    """Modifier une ville"""
    ville = get_object_or_404(Ville, pk=pk)
    villes = Ville.objects.all()
    if request.method == "POST":
        form = VilleForm(request.POST, instance=ville)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.libelle) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "La ville a été modifiée avec succès !")
            return redirect('parametrage:ajouter_ville')
    else:
        form = VilleForm(instance=ville)
    return render(request, 'backend/pages/parametrage/liste_villes.html', {
        'form': form,
        'villes': villes,
        'modifier': True,
        'ville_mod': ville,
    })


@login_required
def supprimer_ville(request, pk):
    """Supprimer une ville"""
    ville = get_object_or_404(Ville, pk=pk)
    ville.delete()
    messages.success(request, "La ville a été supprimée avec succès !")
    return redirect('parametrage:ajouter_ville')


@login_required
def liste_villes(request):
    """Lister toutes les villes"""
    villes = Ville.objects.all()
    form = VilleForm()
    return render(request, 'backend/pages/parametrage/liste_villes.html', {
        'villes': villes,
        'form': form,
        'modifier': False,
    })


# ==========================================
# SITES
# ==========================================
@login_required
def ajouter_site(request):
    """Ajouter un site"""
    form = SiteForm()
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom_site) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "Le site a été ajouté avec succès !")
            return redirect('parametrage:liste_sites')
    sites = Site.objects.all()
    return render(request, 'backend/pages/parametrage/liste_sites.html', {
        'form': form,
        'sites': sites,
        'modifier': False,
    })


@login_required
def modifier_site(request, pk):
    """Modifier un site"""
    site = get_object_or_404(Site, pk=pk)
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in request.POST
        form = SiteForm(post_data, instance=site)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom_site) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "Le site a été modifié avec succès !")
            return redirect('parametrage:liste_sites')
    sites = Site.objects.all()
    return render(request, 'backend/pages/parametrage/liste_sites.html', {
        'sites': sites,
    })


@login_required
def supprimer_site(request, pk):
    """Supprimer un site"""
    site = get_object_or_404(Site, pk=pk)
    site.delete()
    messages.success(request, "Le site a été supprimé.")
    return redirect('parametrage:liste_sites')


@login_required
def liste_sites(request):
    """Lister tous les sites"""
    sites = Site.objects.all()
    form = SiteForm()
    return render(request, 'backend/pages/parametrage/liste_sites.html', {
        'sites': sites,
        'form': form,
        'modifier': False,
    })


# ==========================================
# DÉPARTEMENTS
# ==========================================
@login_required
def ajouter_departement(request):
    """Ajouter un département"""
    form = DepartementForm()
    if request.method == "POST":
        post_data = request.POST.copy()
        form = DepartementForm(post_data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.actif = 'actif' in post_data
            instance.save()
            messages.success(request, "Le département a été ajouté avec succès !")
            return redirect('parametrage:liste_departements')
    departements = Departement.objects.all()
    return render(request, 'backend/pages/parametrage/liste_departements.html', {
        'form': form,
        'departements': departements,
        'modifier': False,
    })


@login_required
def modifier_departement(request, pk):
    """Modifier un département"""
    departement = get_object_or_404(Departement, pk=pk)
    if request.method == "POST":
        form = DepartementForm(request.POST, instance=departement)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.actif = 'actif' in request.POST
            instance.save()
            messages.success(request, "Le département a été modifié avec succès !")
            return redirect('parametrage:liste_departements')
    departements = Departement.objects.all()
    return render(request, 'backend/pages/parametrage/liste_departements.html', {
        'departements': departements,
    })


@login_required
def supprimer_departement(request, pk):
    """Supprimer un département"""
    departement = get_object_or_404(Departement, pk=pk)
    departement.delete()
    messages.success(request, "Le département a été supprimé.")
    return redirect('parametrage:liste_departements')


@login_required
def toggle_departement(request, pk):
    """Activer / désactiver un département"""
    departement = get_object_or_404(Departement, pk=pk)
    departement.actif = not departement.actif
    departement.save()
    status = "activé" if departement.actif else "désactivé"
    messages.success(request, f"Le département a été {status}.")
    return redirect('parametrage:liste_departements')


@login_required
def liste_departements(request):
    """Lister tous les départements"""
    departements = Departement.objects.all()
    form = DepartementForm()
    return render(request, 'backend/pages/parametrage/liste_departements.html', {
        'departements': departements,
        'form': form,
        'modifier': False,
    })


# ==========================================
# SERVICES
# ==========================================
@login_required
def ajouter_service(request):
    """Ajouter un service"""
    departements = Departement.objects.filter(actif=True)
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.actif = 'actif' in request.POST
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "Le service a été ajouté avec succès !")
            return redirect('parametrage:liste_services')
    else:
        form = ServiceForm()
    services = Service.objects.select_related('departement').all()
    return render(request, 'backend/pages/parametrage/liste_services.html', {
        'form': form,
        'services': services,
        'departements': departements,
        'modifier': False,
    })


@login_required
def modifier_service(request, pk):
    """Modifier un service"""
    service = get_object_or_404(Service, pk=pk)
    departements = Departement.objects.filter(actif=True)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.actif = 'actif' in request.POST
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "Le service a été modifié avec succès !")
            return redirect('parametrage:liste_services')
    else:
        form = ServiceForm(instance=service)
    services = Service.objects.select_related('departement').all()
    return render(request, 'backend/pages/parametrage/liste_services.html', {
        'form': form,
        'services': services,
        'departements': departements,
        'modifier': True,
        'service_to_edit': service,
    })


@login_required
def supprimer_service(request, pk):
    """Supprimer un service"""
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, "Le service a été supprimé.")
    return redirect('parametrage:liste_services')


@login_required
def liste_services(request):
    """Lister tous les services"""
    services = Service.objects.all()
    departements = Departement.objects.filter(actif=True)
    form = ServiceForm()
    return render(request, 'backend/pages/parametrage/liste_services.html', {
        'services': services,
        'departements': departements,
        'form': form,
        'modifier': False,
    })

# ==========================================
# FONCTIONS
# ==========================================
@login_required
def ajouter_fonction(request):
    """Ajouter une fonction"""
    if request.method == "POST":
        post_data = request.POST.copy()
        # Checkbox actif : si non cochée, mettre False
        if 'actif' not in post_data:
            post_data['actif'] = False
        form = FonctionForm(post_data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "La fonction a été ajoutée avec succès !")
    return redirect('parametrage:liste_fonctions')


@login_required
def modifier_fonction(request, pk):
    """Modifier une fonction"""
    fonction = get_object_or_404(Fonction, pk=pk)
    if request.method == "POST":
        post_data = request.POST.copy()
        # Checkbox actif : si non cochée, mettre False
        if 'actif' not in post_data:
            post_data['actif'] = False
        form = FonctionForm(post_data, instance=fonction)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()
            messages.success(request, "La fonction a été modifiée avec succès !")
    return redirect('parametrage:liste_fonctions')


@login_required
def supprimer_fonction(request, pk):
    """Supprimer une fonction"""
    fonction = get_object_or_404(Fonction, pk=pk)
    fonction.delete()
    messages.success(request, "La fonction a été supprimée.")
    return redirect('parametrage:liste_fonctions')


@login_required
def liste_fonctions(request):
    """Lister toutes les fonctions"""
    fonctions = Fonction.objects.select_related('service').all()
    services = Service.objects.filter(actif=True)
    form = FonctionForm()
    return render(request, 'backend/pages/parametrage/liste_fonctions.html', {
        'fonctions': fonctions,
        'services': services,
        'form': form,
        'modifier': False,
    })
