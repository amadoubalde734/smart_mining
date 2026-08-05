from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.dateformat import DateFormat
import json
import secrets

# Models & Forms
from .models import Employe
from .forms import EmployeForm
from parametrage.models import Societe, Departement, Service, Fonction, Site, Ville, EmailSettings


# ===============================
# EMPLOYÉ CRUD
# ===============================

@login_required
def employe_list(request):
    employes = Employe.objects.select_related(
        'societe', 'departement', 'service', 'site', 'ville', 'responsable'
    ).all()
    return render(request, 'backend/pages/personnel/employe_list.html', {'employes': employes})


@login_required
def employe_create(request):
    if request.method == "POST":
        form = EmployeForm(request.POST, request.FILES)
        if form.is_valid():
            employe = form.save(commit=False)
            # Génération slug unique
            if not employe.slug:
                employe.slug = employe.generate_unique_slug(
                    f"{employe.nom}-{employe.prenoms}-{employe.matricule}", Employe.objects
                )
            employe.save()
            messages.success(request, f"L'employé {employe.nom} {employe.prenoms} a été ajouté avec succès !")
            return redirect('personnel:employe_list')
    else:
        form = EmployeForm()
    return render(request, 'backend/pages/personnel/employe_create.html', {'form': form})


@login_required
def employe_update(request, slug):
    employe = get_object_or_404(Employe, slug=slug)
    if request.method == "POST":
        form = EmployeForm(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            employe = form.save(commit=False)
            # Si le slug est vide ou modifié
            if not employe.slug:
                employe.slug = employe.generate_unique_slug(
                    f"{employe.nom}-{employe.prenoms}-{employe.matricule}", Employe.objects.exclude(pk=employe.pk)
                )
            employe.save()
            messages.success(request, f"L'employé {employe.nom} {employe.prenoms} a été modifié avec succès !")
            return redirect('personnel:employe_list')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'backend/pages/personnel/employe_update.html', {'form': form, 'employe': employe})


@login_required
def employe_delete(request, slug):
    employe = get_object_or_404(Employe, slug=slug)
    if request.method == "POST":
        employe.delete()
        messages.success(request, f"L'employé {employe.nom} {employe.prenoms} a été supprimé.")
        return redirect('personnel:employe_list')
    return render(request, 'backend/pages/personnel/employe_delete.html', {'employe': employe})


# ===============================
# AJAX
# ===============================

@login_required
def get_services_by_departement(request):
    departement_id = request.GET.get('departement_id')
    services = []
    if departement_id:
        services_qs = Service.objects.filter(departement_id=departement_id, actif=True).order_by('nom')
        services = [{"id": s.id, "nom": s.nom} for s in services_qs]
    return JsonResponse({"services": services})


@login_required
def get_fonctions_by_service(request):
    service_id = request.GET.get('service_id')
    fonctions = []
    if service_id:
        fonctions_qs = Fonction.objects.filter(service_id=service_id, actif=True).order_by('nom')
        fonctions = [{"id": f.id, "nom": f.nom} for f in fonctions_qs]
    return JsonResponse({"fonctions": fonctions})


# ===============================
# DASHBOARD EMPLOYÉS
# ===============================

@login_required
def employe_dashboard(request):
    total_employes = Employe.objects.count()
    total_actifs = Employe.objects.filter(actif=True).count()
    total_inactifs = Employe.objects.filter(actif=False).count()
    hommes = Employe.objects.filter(sexe='M').count()
    femmes = Employe.objects.filter(sexe='F').count()

    repartition_societe = Employe.objects.values('societe__libelle').annotate(total=Count('id')).order_by('societe__libelle')
    repartition_departement = Employe.objects.values('departement__nom').annotate(total=Count('id')).order_by('departement__nom')

    derniers_employes = Employe.objects.order_by('-created_at')[:5]

    evolution_qs = Employe.objects.annotate(mois=TruncMonth('created_at')).values('mois').annotate(total=Count('id')).order_by('mois')
    evolution_dates = [DateFormat(e['mois']).format('M Y') for e in evolution_qs]
    evolution_employes = [e['total'] for e in evolution_qs]

    return render(request, 'backend/pages/personnel/employe_dashboard.html', {
        'total_employes': total_employes,
        'total_actifs': total_actifs,
        'total_inactifs': total_inactifs,
        'hommes': hommes,
        'femmes': femmes,
        'repartition_societe': repartition_societe,
        'repartition_departement': repartition_departement,
        'derniers_employes': derniers_employes,
        'evolution_dates': json.dumps(evolution_dates),
        'evolution_employes': json.dumps(evolution_employes),
    })


# ===============================
# PROFIL & HISTORIQUE
# ===============================

@login_required
def employe_profil(request, slug):
    employe = get_object_or_404(Employe, slug=slug)
    return render(request, 'backend/pages/personnel/employe_profil.html', {'employe': employe})


@login_required
def employe_historique(request, slug):
    employe = get_object_or_404(Employe, slug=slug)
    historique = [
        f"Création de l'employé le {employe.created_at.strftime('%d/%m/%Y %H:%M')}",
        f"Dernière modification le {employe.updated_at.strftime('%d/%m/%Y %H:%M')}",
    ]
    # Tu peux plus tard ajouter l'historique réel depuis HistoriqueEmploye
    return render(request, 'backend/pages/personnel/employe_historique.html', {'employe': employe, 'historique': historique})
