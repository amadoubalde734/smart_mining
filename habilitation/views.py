# habilitation/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import secrets

from .models import (
    FormationChauffeur,
    SuiviPASSMine,
    PermisTravail,
    ComportementConduite
)
from .forms import (
    FormationChauffeurForm,
    SuiviPASSMineForm,
    PermisTravailForm,
    ComportementConduiteForm
)
from documents.models import FichierJoint

# ===============================
# UTILITAIRE POUR CREATE/UPDATE
# ===============================
def save_with_slug(form, slug_field, slug_base):
    """Sauvegarde l'objet en générant un slug si nécessaire"""
    obj = form.save(commit=False)
    if not getattr(obj, slug_field):
        setattr(obj, slug_field, slugify(slug_base) + '-' + secrets.token_urlsafe(5))
    obj.save()
    return obj

# ===============================
# FORMATION CHAUFFEUR
# ===============================
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta  # IMPORTANT : pour ajouter des mois

@login_required
def formation_list(request):
    formations = FormationChauffeur.objects.select_related('employe', 'formateur').all()

    # ----------------------------
    #  WIDGETS : Statistiques
    # ----------------------------
    total_formations = formations.count()

    # Formations récentes (30 jours)
    recent_date = timezone.now() - timedelta(days=30)
    recent_formations = formations.filter(date_formation__gte=recent_date).count()

    # Calcul des expirations
    expired_count = 0
    valid_count = 0
    now = timezone.now().date()

    for f in formations:
        if f.validite:
            expiration = f.validite  # On prend directement la date de validité
            if expiration < now:
                expired_count += 1
            else:
                valid_count += 1
        else:
            valid_count += 1

    context = {
        'formations': formations,
        'total_formations': total_formations,
        'recent_formations': recent_formations,
        'valid_formations': valid_count,
        'expired_formations': expired_count,
    }

    return render(
        request,
        'backend/pages/habilitation/formation/formation_list.html',
        context
    )

# ===============================
# Création d'une formation
# ===============================
@login_required
def formation_create(request):
    form = FormationChauffeurForm(request.POST or None)
    if form.is_valid():
        employe = form.cleaned_data['employe']
        type_formation = form.cleaned_data['type_formation']
        date_formation = form.cleaned_data['date_formation']
        slug_base = f"{employe.nom}-{type_formation.nom}-{date_formation}"
        formation = save_with_slug(form, 'slug', slug_base)
        messages.success(request, f"Formation de {formation.employe} ajoutée !")
        return redirect('habilitation:formation_list')
    return render(
        request,
        'backend/pages/habilitation/formation/formation_create.html',
        {'form': form}
    )

# ===============================
# Mise à jour d'une formation
# ===============================
@login_required
def formation_update(request, slug):
    formation = get_object_or_404(FormationChauffeur, slug=slug)
    form = FormationChauffeurForm(request.POST or None, instance=formation)
    if form.is_valid():
        employe = form.cleaned_data['employe']
        type_formation = form.cleaned_data['type_formation']
        date_formation = form.cleaned_data['date_formation']
        slug_base = f"{employe.nom}-{type_formation.nom}-{date_formation}"
        formation = save_with_slug(form, 'slug', slug_base)
        messages.success(request, f"Formation de {formation.employe} modifiée !")
        return redirect('habilitation:formation_list')
    return render(
        request,
        'backend/pages/habilitation/formation/formation_update.html',
        {'form': form, 'formation': formation}
    )

# ===============================
# Suppression d'une formation
# ===============================
@login_required
def formation_delete(request, slug):
    formation = get_object_or_404(FormationChauffeur, slug=slug)
    if request.method == "POST":
        formation.delete()
        messages.success(request, f"Formation de {formation.employe} supprimée !")
        return redirect('habilitation:formation_list')
    return render(
        request,
        'backend/pages/habilitation/formation/formation_delete.html',
        {'formation': formation}
    )

# ===============================
# LISTE DES PASS
# ===============================
@login_required
def pass_list(request):
    passes = SuiviPASSMine.objects.select_related("employe", "responsable", "site_emission").all()

    today = date.today()
    last_30_days = today - timedelta(days=30)

    total_pass = passes.count()
    recent_pass = passes.filter(date_emission__gte=last_30_days).count()
    valid_pass = passes.filter(date_expiration__gte=today).count()
    expired_pass = passes.filter(date_expiration__lt=today).count()

    context = {
        "passes": passes,
        "total_pass": total_pass,
        "recent_pass": recent_pass,
        "valid_pass": valid_pass,
        "expired_pass": expired_pass,
    }
    return render(request, "backend/pages/habilitation/passmine/pass_list.html", context)

# ===============================
# CREATION DE PASS
# ===============================
@login_required
def pass_create(request):
    form = SuiviPASSMineForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # Sauvegarde avec génération de slug
        p = save_with_slug(form, 'slug', f"{form.cleaned_data['employe'].nom}-{form.cleaned_data['numero_pass']}")

        # Gestion des fichiers joints
        fichiers = request.FILES.getlist('fichiers_joints')
        for f in fichiers:
            FichierJoint.objects.create(titre=f.name, fichier=f, content_object=p)

        messages.success(request, f"PASS de {p.employe} ajoutée avec succès !")
        return redirect('habilitation:pass_list')

    return render(request, 'backend/pages/habilitation/passmine/pass_create.html', {'form': form})

# ===============================
# MISE À JOUR DE PASS
# ===============================
@login_required
def pass_update(request, slug):
    p = get_object_or_404(SuiviPASSMine, slug=slug)
    form = SuiviPASSMineForm(request.POST or None, request.FILES or None, instance=p)

    if form.is_valid():
        p = save_with_slug(form, 'slug', f"{form.cleaned_data['employe'].nom}-{form.cleaned_data['numero_pass']}")

        # Gestion des fichiers joints supplémentaires
        fichiers = request.FILES.getlist('fichiers_joints')
        for f in fichiers:
            FichierJoint.objects.create(titre=f.name, fichier=f, content_object=p)

        messages.success(request, f"PASS de {p.employe} modifiée avec succès !")
        return redirect('habilitation:pass_list')

    context = {
        'form': form,
        'pass': p
    }
    return render(request, 'backend/pages/habilitation/passmine/pass_update.html', context)

# ===============================
# SUPPRESSION DE PASS
# ===============================
@login_required
def pass_delete(request, slug):
    p = get_object_or_404(SuiviPASSMine, slug=slug)
    if request.method == "POST":
        p.delete()
        messages.success(request, f"PASS de {p.employe} supprimée avec succès !")
        return redirect('habilitation:pass_list')

    return render(request, 'backend/pages/habilitation/passmine/pass_delete.html', {'pass': p})

# ===============================
# LISTE DES PERMIS
# ===============================
@login_required
def permis_list(request):
    permis = PermisTravail.objects.select_related('employe', 'type_permis').all()

    today = date.today()
    last_30 = today - timedelta(days=30)

    context = {
        'permis': permis,
        'total_permis': permis.count(),
        'recent_permis': permis.filter(date_emission__gte=last_30).count(),
        'valid_permis': permis.filter(date_expiration__gte=today).count(),
        'expired_permis': permis.filter(date_expiration__lt=today).count(),
        'today': today,
    }

    return render(request, 'backend/pages/habilitation/permis_travail/permis_list.html', context)


# ===============================
# CREATION D'UN PERMIS
# ===============================
@login_required
def permis_create(request):
    form = PermisTravailForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        perm = save_with_slug(
            form, 'slug',
            f"{form.cleaned_data['employe'].nom}-{form.cleaned_data['type_permis'].nom}-{str(form.cleaned_data['date_emission'])}"
        )
        # Gestion des fichiers joints
        fichiers = request.FILES.getlist('fichiers_joints')
        for f in fichiers:
            FichierJoint.objects.create(titre=f.name, fichier=f, content_object=perm)
        messages.success(request, f"Permis de {perm.employe} ajouté !")
        return redirect('habilitation:permis_list')

    return render(request, 'backend/pages/habilitation/permis_travail/permis_create.html', {'form': form})


# ===============================
# MISE À JOUR D'UN PERMIS
# ===============================
@login_required
def permis_update(request, slug):
    perm = get_object_or_404(PermisTravail, slug=slug)
    form = PermisTravailForm(request.POST or None, request.FILES or None, instance=perm)
    if form.is_valid():
        perm = save_with_slug(
            form, 'slug',
            f"{form.cleaned_data['employe'].nom}-{form.cleaned_data['type_permis'].nom}-{str(form.cleaned_data['date_emission'])}"
        )
        # Gestion des fichiers joints
        fichiers = request.FILES.getlist('fichiers_joints')
        for f in fichiers:
            FichierJoint.objects.create(titre=f.name, fichier=f, content_object=perm)
        messages.success(request, f"Permis de {perm.employe} modifié !")
        return redirect('habilitation:permis_list')

    return render(request, 'backend/pages/habilitation/permis_travail/permis_update.html', {'form': form, 'permis': perm})


# ===============================
# SUPPRESSION D'UN PERMIS
# ===============================
@login_required
def permis_delete(request, slug):
    perm = get_object_or_404(PermisTravail, slug=slug)
    if request.method == "POST":
        perm.delete()
        messages.success(request, f"Permis de {perm.employe} supprimé !")
        return redirect('habilitation:permis_list')

    return render(request, 'backend/pages/habilitation/permis_travail/permis_delete.html', {'permis': perm})

# ===============================
# COMPORTEMENT ET CONDUITE
# ===============================
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ComportementConduite, FichierJoint
from .forms import ComportementConduiteForm

@login_required
def conduite_list(request):
    comportements = ComportementConduite.objects.select_related(
        'employe', 'responsable', 'evaluateur'
    ).all()

    today = date.today()
    last_30 = today - timedelta(days=30)

    total_evaluations = comportements.count()
    recent_evaluations = comportements.filter(date_evaluation__gte=last_30).count()
    valid_evaluations = comportements.filter(score__gte=50).count()
    low_score_evaluations = comportements.filter(score__lt=50).count()

    context = {
        'comportements': comportements,
        'total_evaluations': total_evaluations,
        'recent_evaluations': recent_evaluations,
        'valid_evaluations': valid_evaluations,
        'low_score_evaluations': low_score_evaluations,
        'today': today,
    }

    return render(request, 'backend/pages/habilitation/comportement/conduite_list.html', context)


@login_required
def conduite_create(request):
    form = ComportementConduiteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        comp = save_with_slug(
            form, 'slug', f"{form.cleaned_data['employe'].nom}-{form.cleaned_data['date_evaluation']}"
        )
        # Gestion des fichiers joints
        fichiers = request.FILES.getlist('fichiers_joints')
        for f in fichiers:
            FichierJoint.objects.create(titre=f.name, fichier=f, content_object=comp)
        messages.success(request, f"Évaluation de {comp.employe} ajoutée !")
        return redirect('habilitation:conduite_list')

    return render(
        request,
        'backend/pages/habilitation/comportement/conduite_create.html',
        {'form': form}
    )

@login_required
def conduite_update(request, slug):
    comp = get_object_or_404(ComportementConduite, slug=slug)
    form = ComportementConduiteForm(request.POST or None, request.FILES or None, instance=comp)
    if form.is_valid():
        comp = save_with_slug(
            form, 'slug', f"{form.cleaned_data['employe'].nom}-{form.cleaned_data['date_evaluation']}"
        )
        # Gestion des fichiers joints
        fichiers = request.FILES.getlist('fichiers_joints')
        for f in fichiers:
            FichierJoint.objects.create(titre=f.name, fichier=f, content_object=comp)
        messages.success(request, f"Évaluation de {comp.employe} modifiée !")
        return redirect('habilitation:conduite_list')

    return render(
        request,
        'backend/pages/habilitation/comportement/conduite_update.html',
        {'form': form, 'comportement': comp}
    )


@login_required
def conduite_delete(request, slug):
    comp = get_object_or_404(ComportementConduite, slug=slug)
    if request.method == "POST":
        comp.delete()
        messages.success(request, f"Évaluation de {comp.employe} supprimée !")
        return redirect('habilitation:conduite_list')

    return render(
        request,
        'backend/pages/habilitation/comportement/conduite_delete.html',
        {'comportement': comp}
    )

# ===============================
# HISTORIQUE HABILLITATION
# ===============================
from .models import HistoriqueHabilitation

@login_required
def historique_list(request):
    """
    Affiche la liste des historiques pour tous les modèles habilitation.
    Possibilité de filtrer par utilisateur ou type d'action via GET.
    """
    historiques = HistoriqueHabilitation.objects.select_related('utilisateur', 'content_type').all()

    # Filtres optionnels
    utilisateur_id = request.GET.get('utilisateur')
    action = request.GET.get('action')

    if utilisateur_id:
        historiques = historiques.filter(utilisateur_id=utilisateur_id)
    if action:
        historiques = historiques.filter(action=action)

    context = {
        'historiques': historiques,
    }
    return render(request, 'backend/pages/habilitation/historique_list.html', context)

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from datetime import date, timedelta
# from dateutil.relativedelta import relativedelta

# from .models import (
#     IdentificationEmploye,
#     FormationChauffeur,
#     SuiviPASSMine,
#     PermisTravail,
#     ComportementConduite
# )

# @login_required
# def dashboard_habilitation(request):
#     today = date.today()
#     last_30 = today - timedelta(days=30)

#     # =====================
#     # Identification Employés
#     # =====================
#     identifications = IdentificationEmploye.objects.all()
#     identifications_stats = [
#         {'title': 'Total Identifications', 'value': identifications.count(), 'icon': 'bx-id-card', 'color': 'primary'},
#         {'title': 'Récentes (7j)', 'value': identifications.filter(date_identification__gte=today - timedelta(days=7)).count(), 'icon': 'bx-timer', 'color': 'success'},
#         {'title': 'Actives', 'value': identifications.filter(actif=True).count(), 'icon': 'bx-check-circle', 'color': 'info'},
#         {'title': 'Inactives', 'value': identifications.filter(actif=False).count(), 'icon': 'bx-x-circle', 'color': 'danger'},
#     ]

#     # =====================
#     # Formations Chauffeur
#     # =====================
#     formations = FormationChauffeur.objects.all()
#     valid_formations = expired_formations = 0
#     for f in formations:
#         if f.validite:
#             expiration = f.date_formation + relativedelta(months=f.validite)
#             if expiration < today:
#                 expired_formations += 1
#             else:
#                 valid_formations += 1
#         else:
#             valid_formations += 1

#     formations_stats = [
#         {'title': 'Total Formations', 'value': formations.count(), 'icon': 'bx-book', 'color': 'primary'},
#         {'title': 'Récentes (30j)', 'value': formations.filter(date_formation__gte=today - timedelta(days=30)).count(), 'icon': 'bx-timer', 'color': 'success'},
#         {'title': 'Valides', 'value': valid_formations, 'icon': 'bx-check-circle', 'color': 'info'},
#         {'title': 'Expirées', 'value': expired_formations, 'icon': 'bx-x-circle', 'color': 'danger'},
#     ]

#     # =====================
#     # PASS Mine
#     # =====================
#     passes = SuiviPASSMine.objects.all()
#     pass_stats = [
#         {'title': 'Total PASS', 'value': passes.count(), 'icon': 'bx-id-card', 'color': 'primary'},
#         {'title': 'Récentes (30j)', 'value': passes.filter(date_emission__gte=last_30).count(), 'icon': 'bx-timer', 'color': 'success'},
#         {'title': 'Valides', 'value': passes.filter(date_expiration__gte=today).count(), 'icon': 'bx-check-circle', 'color': 'info'},
#         {'title': 'Expirées', 'value': passes.filter(date_expiration__lt=today).count(), 'icon': 'bx-x-circle', 'color': 'danger'},
#     ]

#     # =====================
#     # Permis de Travail
#     # =====================
#     permis = PermisTravail.objects.all()
#     permis_stats = [
#         {'title': 'Total Permis', 'value': permis.count(), 'icon': 'bx-id-card', 'color': 'primary'},
#         {'title': 'Récentes (30j)', 'value': permis.filter(date_emission__gte=last_30).count(), 'icon': 'bx-timer', 'color': 'success'},
#         {'title': 'Valides', 'value': permis.filter(date_expiration__gte=today).count(), 'icon': 'bx-check-circle', 'color': 'info'},
#         {'title': 'Expirées', 'value': permis.filter(date_expiration__lt=today).count(), 'icon': 'bx-x-circle', 'color': 'danger'},
#     ]

#     # =====================
#     # Conduite
#     # =====================
#     comportements = ComportementConduite.objects.all()
#     conduite_stats = [
#         {'title': 'Total Évaluations', 'value': comportements.count(), 'icon': 'bx-book', 'color': 'primary'},
#         {'title': 'Récentes (30j)', 'value': comportements.filter(date_evaluation__gte=last_30).count(), 'icon': 'bx-timer', 'color': 'success'},
#         {'title': 'Valides (≥50%)', 'value': comportements.filter(score__gte=50).count(), 'icon': 'bx-check-circle', 'color': 'info'},
#         {'title': 'Scores Faibles (<50%)', 'value': comportements.filter(score__lt=50).count(), 'icon': 'bx-x-circle', 'color': 'danger'},
#     ]

#     context = {
#         'identifications_stats': identifications_stats,
#         'formations_stats': formations_stats,
#         'pass_stats': pass_stats,
#         'permis_stats': permis_stats,
#         'conduite_stats': conduite_stats,
#     }

#     return render(request, 'backend/pages/habilitation/dashboard_habilitation.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from .models import (
    FormationChauffeur,
    SuiviPASSMine,
    PermisTravail,
    ComportementConduite
)

@login_required
def dashboard_habilitation(request):
    today = date.today()
    last_30 = today - timedelta(days=30)

    # =====================
    # Récupérer les filtres depuis GET
    # =====================
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = date.fromisoformat(start_date)
    if end_date:
        end_date = date.fromisoformat(end_date)

    # =====================
    # Formations Chauffeur
    # =====================
    formations = FormationChauffeur.objects.all()
    if start_date and end_date:
        formations = formations.filter(date_formation__range=(start_date, end_date))

    valid_formations = expired_formations = 0
    for f in formations:
        if f.validite:
            expiration = f.date_formation + relativedelta(months=f.validite)
            if expiration < today:
                expired_formations += 1
            else:
                valid_formations += 1
        else:
            valid_formations += 1

    formations_stats = [
        {'title': 'Total Formations', 'value': formations.count(), 'icon': 'bx-book', 'color': 'primary'},
        {'title': 'Récentes (30j)', 'value': formations.filter(date_formation__gte=today - timedelta(days=30)).count(), 'icon': 'bx-timer', 'color': 'success'},
        {'title': 'Valides', 'value': valid_formations, 'icon': 'bx-check-circle', 'color': 'info'},
        {'title': 'Expirées', 'value': expired_formations, 'icon': 'bx-x-circle', 'color': 'danger'},
    ]

    # =====================
    # PASS Mine
    # =====================
    passes = SuiviPASSMine.objects.all()
    if start_date and end_date:
        passes = passes.filter(date_emission__range=(start_date, end_date))

    pass_stats = [
        {'title': 'Total PASS', 'value': passes.count(), 'icon': 'bx-id-card', 'color': 'primary'},
        {'title': 'Récentes (30j)', 'value': passes.filter(date_emission__gte=last_30).count(), 'icon': 'bx-timer', 'color': 'success'},
        {'title': 'Valides', 'value': passes.filter(date_expiration__gte=today).count(), 'icon': 'bx-check-circle', 'color': 'info'},
        {'title': 'Expirées', 'value': passes.filter(date_expiration__lt=today).count(), 'icon': 'bx-x-circle', 'color': 'danger'},
    ]

    # =====================
    # Permis de Travail
    # =====================
    permis = PermisTravail.objects.all()
    if start_date and end_date:
        permis = permis.filter(date_emission__range=(start_date, end_date))

    permis_stats = [
        {'title': 'Total Permis', 'value': permis.count(), 'icon': 'bx-id-card', 'color': 'primary'},
        {'title': 'Récentes (30j)', 'value': permis.filter(date_emission__gte=last_30).count(), 'icon': 'bx-timer', 'color': 'success'},
        {'title': 'Valides', 'value': permis.filter(date_expiration__gte=today).count(), 'icon': 'bx-check-circle', 'color': 'info'},
        {'title': 'Expirées', 'value': permis.filter(date_expiration__lt=today).count(), 'icon': 'bx-x-circle', 'color': 'danger'},
    ]

    # =====================
    # Conduite
    # =====================
    comportements = ComportementConduite.objects.all()
    if start_date and end_date:
        comportements = comportements.filter(date_evaluation__range=(start_date, end_date))

    conduite_stats = [
        {'title': 'Total Évaluations', 'value': comportements.count(), 'icon': 'bx-book', 'color': 'primary'},
        {'title': 'Récentes (30j)', 'value': comportements.filter(date_evaluation__gte=last_30).count(), 'icon': 'bx-timer', 'color': 'success'},
        {'title': 'Valides (≥50%)', 'value': comportements.filter(score__gte=50).count(), 'icon': 'bx-check-circle', 'color': 'info'},
        {'title': 'Scores Faibles (<50%)', 'value': comportements.filter(score__lt=50).count(), 'icon': 'bx-x-circle', 'color': 'danger'},
    ]

    # =====================
    # Sections pour le template
    # =====================
    sections = [
        {
            'id': 'formations',
            'title': 'Formations Chauffeur',
            'stats': formations_stats,
            'chart_type': 'doughnut',
            'chart_labels': ['Valides', 'Expirées'],
            'chart_data': [formations_stats[2]['value'], formations_stats[3]['value']],
            'chart_colors': ['#198754', '#dc3545'],
        },
        {
            'id': 'pass',
            'title': 'PASS Mine',
            'stats': pass_stats,
            'chart_type': 'doughnut',
            'chart_labels': ['Valides', 'Expirées'],
            'chart_data': [pass_stats[2]['value'], pass_stats[3]['value']],
            'chart_colors': ['#0dcaf0', '#dc3545'],
        },
        {
            'id': 'permis',
            'title': 'Permis de Travail',
            'stats': permis_stats,
            'chart_type': 'doughnut',
            'chart_labels': ['Valides', 'Expirés'],
            'chart_data': [permis_stats[2]['value'], permis_stats[3]['value']],
            'chart_colors': ['#0d6efd', '#dc3545'],
        },
        {
            'id': 'conduite',
            'title': 'Évaluations Conduite',
            'stats': conduite_stats,
            'chart_type': 'bar',
            'chart_label': 'Évaluations',
            'chart_labels': ['Valides (≥50%)', 'Scores Faibles (<50%)'],
            'chart_data': [conduite_stats[2]['value'], conduite_stats[3]['value']],
            'chart_colors': ['#198754', '#dc3545'],
        },
    ]

    return render(request, 'backend/pages/habilitation/dashboard_habilitation.html', {
        'sections': sections,
        'start_date': start_date,
        'end_date': end_date,
    })
