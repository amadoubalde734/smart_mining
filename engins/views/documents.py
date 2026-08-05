# =========================
# Django utilities
# =========================
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models import Count, Q

# =========================
# MODELS
# =========================
from engins.models import (
    Engin,
    Remorque,
    Citerne,
    AssuranceEngin,
    VignetteConformite,
    ControleTechnique,
    CertificatJaugeage,
    SiteEngin
)
from engins.models.documents_legaux import CarteGrise
from documents.models import FichierJoint
# =========================
# FORMS
# =========================
from engins.forms.documents import (
    CarteGriseForm,
    AssuranceEnginForm,
    VignetteConformiteForm,
    ControleTechniqueForm,
    ControleTechniqueDocumentForm,
    CertificatJaugeageForm,
    CertificatJaugeageDocumentForm
)
from documents.forms import FichierJointForm
# ===============================
# LISTE DES ASSURANCES (avec création via modal)
# ===============================
@login_required
def assurance_list(request):
    assurances = AssuranceEngin.objects.select_related('engin').all()

    # Gestion du POST pour création via modal
    if request.method == "POST":
        nom = request.POST.get("nom")
        type_assurance = request.POST.get("type_assurance")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        observations = request.POST.get("observations")
        engin_id = request.POST.get("engin")

        engin = Engin.objects.get(id=engin_id) if engin_id else None

        if engin and nom and type_assurance and date_debut and date_fin:
            AssuranceEngin.objects.create(
                nom=nom,
                type_assurance=type_assurance,
                date_debut=date_debut,
                date_fin=date_fin,
                observations=observations,
                engin=engin
            )
            messages.success(request, "Assurance ajoutée avec succès.")
            return redirect('assurance:assurance_list')
        else:
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")

    # Stats
    total_assurances = assurances.count()
    valid_assurances = assurances.filter(date_fin__gte=timezone.now()).count()
    expired_assurances = assurances.filter(date_fin__lt=timezone.now()).count()

    all_engins = Engin.objects.all()
    assurance_types = AssuranceEngin.ASSURANCE_TYPES

    context = {
        "assurances": assurances,
        "total_assurances": total_assurances,
        "valid_assurances": valid_assurances,
        "expired_assurances": expired_assurances,
        "all_engins": all_engins,
        "assurance_types": assurance_types,
    }
    return render(request, 'backend/pages/engins/engins/assurance_list.html', context)

# ===============================
# MISE À JOUR D'UNE ASSURANCE
# ===============================
@login_required
def assurance_update(request, pk):
    assurance = get_object_or_404(AssuranceEngin, pk=pk)

    if request.method == "POST":
        form = AssuranceEnginForm(request.POST, instance=assurance)
        if form.is_valid():
            form.save()
            messages.success(request, "Assurance modifiée avec succès.")
            return redirect('assurance:assurance_list')
        else:
            messages.error(request, "Erreur lors de la modification de l'assurance.")
    else:
        form = AssuranceEnginForm(instance=assurance)

    all_engins = Engin.objects.all()
    assurance_types = AssuranceEngin.ASSURANCE_TYPES

    return render(request, 'backend/pages/engins/engins/assurance_update.html', {
        'form': form,
        'assurance': assurance,
        'all_engins': all_engins,
        'assurance_types': assurance_types,
    })


# ===============================
# SUPPRESSION D'UNE ASSURANCE
# ===============================
@login_required
def assurance_delete(request, pk):
    assurance = get_object_or_404(AssuranceEngin, pk=pk)

    if request.method == "POST":
        assurance.delete()
        messages.success(request, "Assurance supprimée avec succès.")
        return redirect('assurance:assurance_list')

    return render(request, 'backend/pages/engins/engins/assurance_delete.html', {
        'assurance': assurance
    })

# ===============================
# LISTE DES VIGNETTES
# ===============================
def vignettes_list(request):
    vignettes = VignetteConformite.objects.select_related('engin').all()

    # Gestion du POST depuis le modal
    if request.method == "POST":
        engin_id = request.POST.get("engin")
        type_vignette = request.POST.get("type_vignette")
        date_emission = request.POST.get("date_emission")
        date_expire = request.POST.get("date_expire")
        observations = request.POST.get("observations")

        vignette = VignetteConformite.objects.create(
            engin=Engin.objects.get(id=engin_id) if engin_id else None,
            type_vignette=type_vignette,
            date_emission=date_emission,
            date_expire=date_expire,
            observations=observations
        )

        messages.success(request, "Vignette ajoutée avec succès.")
        return redirect("vignette:vignettes_list")

    # Statistiques
    total_vignettes = vignettes.count()
    valid_vignettes = vignettes.filter(date_expire__gte=timezone.now()).count()
    expired_vignettes = vignettes.filter(date_expire__lt=timezone.now()).count()

    all_engins = Engin.objects.all()
    vignette_types = VignetteConformite.TYPES_VIGNETTE

    context = {
        "vignettes": vignettes,
        "total_vignettes": total_vignettes,
        "valid_vignettes": valid_vignettes,
        "expired_vignettes": expired_vignettes,
        "all_engins": all_engins,
        "vignette_types": vignette_types,
    }

    return render(request, 'backend/pages/engins/engins/vignette_conformite.html', context)

# ===============================
# MISE À JOUR D'UNE VIGNETTE
# ===============================
def vignette_update(request, pk):
    vignette = get_object_or_404(VignetteConformite, pk=pk)

    if request.method == "POST":
        vignette.engin_id = request.POST.get("engin")
        vignette.type_vignette = request.POST.get("type_vignette")
        vignette.date_emission = request.POST.get("date_emission")
        vignette.date_expire = request.POST.get("date_expire")
        vignette.observations = request.POST.get("observations")
        vignette.save()

        messages.success(request, "Vignette modifiée avec succès.")
        return redirect("vignette:vignettes_list")

    all_engins = Engin.objects.all()
    vignette_types = VignetteConformite.TYPES_VIGNETTE

    return render(request, 'backend/pages/engins/engins/vignette_update.html', {
        "vignette": vignette,
        "all_engins": all_engins,
        "vignette_types": vignette_types,
    })

# ===============================
# SUPPRESSION D'UNE VIGNETTE
# ===============================
def vignette_delete(request, pk):
    vignette = get_object_or_404(VignetteConformite, pk=pk)

    if request.method == "POST":
        vignette.delete()
        messages.success(request, "Vignette supprimée avec succès.")
        return redirect("vignette:vignettes_list")

    return render(request, 'backend/pages/engins/engins/vignette_delete.html', {
        "vignette": vignette
    })

# ===============================
# LISTE DES CONTRÔLES TECHNIQUES
# ===============================
def controles_list(request):
    controles = ControleTechnique.objects.select_related('engin').all()

    total_controles = controles.count()
    valid_controles = controles.filter(en_validite=True).count()
    expired_controles = controles.filter(en_validite=False).count()

    context = {
        'controles': controles,
        'total_controles': total_controles,
        'valid_controles': valid_controles,
        'expired_controles': expired_controles,
    }
    return render(request, 'backend/pages/engins/engins/controle_technique_list.html', context)

# ===============================
# AJOUT D'UN CONTRÔLE
# ===============================
def controle_create(request):
    if request.method == "POST":
        form = ControleTechniqueForm(request.POST, request.FILES)
        doc_form = ControleTechniqueDocumentForm(request.POST, request.FILES)
        if form.is_valid() and doc_form.is_valid():
            controle = form.save()

            # Sauvegarde du document et association avec le contrôle
            doc = doc_form.save(commit=False)
            doc.content_object = controle
            doc.save()

            messages.success(request, "Contrôle technique ajouté avec succès.")
            return redirect('flotte:controle_technique')
        else:
            messages.error(request, "Erreur lors de l'ajout du contrôle.")
    else:
        form = ControleTechniqueForm()
        doc_form = ControleTechniqueDocumentForm()

    return render(
        request,
        'backend/pages/engins/engins/controle_create.html',
        {'form': form, 'doc_form': doc_form}
    )

# ===============================
# MISE À JOUR D'UN CONTRÔLE
# ===============================
def controle_update(request, pk):
    controle = get_object_or_404(ControleTechnique, pk=pk)
    if request.method == "POST":
        form = ControleTechniqueForm(request.POST, request.FILES, instance=controle)
        doc_form = ControleTechniqueDocumentForm(request.POST, request.FILES)
        if form.is_valid() and doc_form.is_valid():
            form.save()

            # Sauvegarde du document et association avec le contrôle
            doc = doc_form.save(commit=False)
            doc.content_object = controle
            doc.save()

            messages.success(request, "Contrôle modifié avec succès.")
            return redirect('engins:controle_technique')
        else:
            messages.error(request, "Erreur lors de la modification du contrôle.")
    else:
        form = ControleTechniqueForm(instance=controle)
        doc_form = ControleTechniqueDocumentForm()

    context = {
        'form': form,
        'doc_form': doc_form,
        'controle': controle,
    }
    return render(request, 'backend/pages/engins/engins/controle_update.html', context)

# ===============================
# SUPPRESSION D'UN CONTRÔLE
# ===============================
def controle_delete(request, pk):
    controle = get_object_or_404(ControleTechnique, pk=pk)
    if request.method == "POST":
        controle.delete()
        messages.success(request, "Contrôle supprimé avec succès.")
        return redirect('flotte:controle_technique')

    return render(request, 'backend/pages/engins/engins/controle_delete.html', {'controle': controle})


# ===============================
# DOCUMENTS LÉGAUX DES ENGINS (avec certificats de jaugeage)
# ===============================

def documents_legaux(request):
    """
    Page principale des documents légaux pour les engins.
    Affiche Assurances, Vignettes, Contrôles techniques et Certificats de jaugeage dans des onglets.
    """
    assurances = AssuranceEngin.objects.select_related('engin').all()
    vignettes = VignetteConformite.objects.select_related('engin').all()
    controles = ControleTechnique.objects.select_related('engin').all()
    certificats = CertificatJaugeage.objects.select_related('engin').all()

    context = {
        'assurances': assurances,
        'vignettes': vignettes,
        'controles': controles,
        'certificats': certificats,
    }
    return render(request, "backend/pages/engins/engins/documents_legaux.html", context)


# =========================================
# LISTE DES CERTIFICATS DE JAUGEAGE
# =========================================
def certificat_jaugeage_list(request):
    certificats = CertificatJaugeage.objects.select_related('engin').all()
    all_engins = Engin.objects.all()

    total_certificats = certificats.count()
    valid_certificats = certificats.filter(en_validite=True).count()
    expired_certificats = certificats.filter(en_validite=False).count()

    context = {
        'certificats': certificats,
        'all_engins': all_engins,
        'total_certificats': total_certificats,
        'valid_certificats': valid_certificats,
        'expired_certificats': expired_certificats,
    }
    return render(request, 'backend/pages/engins/engins/certificat_jaugeage_list.html', context)


# =========================================
# AJOUT D'UN CERTIFICAT DE JAUGEAGE
# =========================================
def certificat_jaugeage_create(request):
    if request.method == "POST":
        form = CertificatJaugeageForm(request.POST, request.FILES)
        doc_form = CertificatJaugeageDocumentForm(request.POST, request.FILES)
        if form.is_valid() and doc_form.is_valid():
            certificat = form.save()
            doc = doc_form.save(commit=False)
            doc.content_object = certificat
            doc.save()
            messages.success(request, "Certificat de jaugeage ajouté avec succès.")
        else:
            messages.error(request, "Erreur lors de l'ajout du certificat.")
        return redirect("engins:certificat_jaugeage_list")  # retour à la liste

    # GET request
    messages.error(request, "Méthode non autorisée.")
    return redirect("engins:certificat_jaugeage_list")


# =========================================
# MISE À JOUR D'UN CERTIFICAT DE JAUGEAGE
# =========================================
def certificat_jaugeage_update(request, pk):
    certificat = get_object_or_404(CertificatJaugeage, pk=pk)

    if request.method == "POST":
        form = CertificatJaugeageForm(request.POST, request.FILES, instance=certificat)
        doc_form = CertificatJaugeageDocumentForm(request.POST, request.FILES)
        if form.is_valid() and doc_form.is_valid():
            form.save()
            doc = doc_form.save(commit=False)
            doc.content_object = certificat
            doc.save()
            messages.success(request, "Certificat modifié avec succès.")
        else:
            messages.error(request, "Erreur lors de la modification du certificat.")
        return redirect("engins:certificat_jaugeage_list")

    # GET request
    messages.error(request, "Méthode non autorisée.")
    return redirect("engins:certificat_jaugeage_list")


# =========================================
# SUPPRESSION D'UN CERTIFICAT DE JAUGEAGE
# =========================================
def certificat_jaugeage_delete(request, pk):
    certificat = get_object_or_404(CertificatJaugeage, pk=pk)
    if request.method == "POST":
        certificat.delete()
        messages.success(request, "Certificat supprimé avec succès.")
        return redirect("engins:certificat_jaugeage_list")

    # GET request
    messages.error(request, "Méthode non autorisée.")
    return redirect("engins:certificat_jaugeage_list")


# engins/views/documents.py (ou views.py)
STATUTS_DOCUMENT = [
    ("VALIDE", "Valide"),
    ("EXPIRE", "Expiré"),
    ("SUSPENDU", "Suspendu"),
]

# ===============================
# LISTE DES CARTES GRISES
# ===============================
@login_required
def carte_grise_list(request):
    cartes = CarteGrise.objects.select_related('engin', 'remorque', 'citerne').all()

    # Statistiques optimisées
    stats = cartes.aggregate(
        total=Count('id'),
        valides=Count('id', filter=Q(statut="VALIDE")),
        expirees=Count('id', filter=Q(statut="EXPIRE")),
    )

    context = {
        "cartes": cartes,
        "total_cartes": stats["total"],
        "valides": stats["valides"],
        "expirees": stats["expirees"],
        "all_engins": Engin.objects.all(),  # pour le modal
    }

    return render(
        request,
        "backend/pages/engins/engins/carte_grise_list.html",
        context
    )


# ===============================
# CRÉATION D'UNE CARTE GRISE
# ===============================
@login_required
def carte_grise_create(request):
    if request.method == "POST":
        form = CarteGriseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Carte grise ajoutée avec succès.")
            return redirect("engins:carte_grise_list")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = CarteGriseForm()

    context = {
        "form": form,
        "all_engins": form.fields['engin'].queryset,  # nécessaire pour ton modal
    }

    return render(
        request,
        "backend/pages/engins/engins/carte_grise_form.html",
        context
    )


# ===============================
# MISE À JOUR D'UNE CARTE GRISE
# ===============================
@login_required
def carte_grise_update(request, pk):
    carte = get_object_or_404(CarteGrise, pk=pk)

    if request.method == "POST":
        form = CarteGriseForm(request.POST, request.FILES, instance=carte)
        if form.is_valid():
            form.save()
            messages.success(request, "Carte grise modifiée avec succès.")
            return redirect("engins:carte_grise_list")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = CarteGriseForm(instance=carte)

    context = {
        "form": form,
        "carte": carte,
    }

    return render(
        request,
        "backend/pages/engins/engins/carte_grise_form.html",
        context
    )


# ===============================
# SUPPRESSION D'UNE CARTE GRISE
# ===============================
@login_required
def carte_grise_delete(request, pk):
    carte = get_object_or_404(CarteGrise, pk=pk)

    if request.method == "POST":
        carte.delete()
        messages.success(request, "Carte grise supprimée avec succès.")
        return redirect("engins:carte_grise_list")

    return HttpResponseForbidden("Méthode non autorisée.")