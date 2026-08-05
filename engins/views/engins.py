# =========================
# Django utilities
# =========================
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# =========================
# MODELS
# =========================
from ..models import (
    Engin,
    TypeEngin,
    CategorieEngin,
    Marque,
    Modele,
    StatutEngin,
    SiteEngin,
    Citerne
)

# =========================
# FORMS PARAMÉTRAGE ENGINS
# =========================
from ..forms.engins import (
    TypeEnginForm,
    CategorieEnginForm,
    MarqueForm,
    ModeleForm,
    StatutEnginForm,
    SiteEnginForm,
    EnginForm,
    RemorqueForm,
    CiterneForm
)

# =========================
# FORMS DOCUMENTS
# =========================
from documents.forms import FichierJointForm

@login_required
def type_list(request):
    types = TypeEngin.objects.all()
    total_types = types.count()
    active_types = types.filter(actif=True).count()
    inactive_types = types.filter(actif=False).count()
    recent_types = types.filter(created_at__gte=timezone.now()-timedelta(days=30)).count()

    context = {
        'types': types,
        'total_types': total_types,
        'active_types': active_types,
        'inactive_types': inactive_types,
        'recent_types': recent_types,
    }
    return render(request, 'backend/pages/engins/types/type_list.html', context)


@login_required
def type_create(request):
    form = TypeEnginForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('engins:type_list')
    return render(request, 'backend/pages/engins/types/type_form.html', {'form': form})

@login_required
def type_update(request, slug):
    obj = get_object_or_404(TypeEngin, slug=slug)
    form = TypeEnginForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('engins:type_list')
    return render(request, 'backend/pages/engins/types/type_form.html', {'form': form, 'modifier': True})

@login_required
def type_delete(request, slug):
    obj = get_object_or_404(TypeEngin, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('engins:type_list')
    return render(request, 'backend/pages/engins/types/confirm_delete.html', {'obj': obj})


# ===============================
# CATEGORIES D'ENGINS
# ===============================
@login_required
def categorie_list(request):
    categories = CategorieEngin.objects.all()

    # Widgets
    total_categories = categories.count()
    active_categories = categories.filter(actif=True).count()
    inactive_categories = categories.filter(actif=False).count()
    
    # Catégories créées dans les 30 derniers jours
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_categories = categories.filter(created_at__gte=thirty_days_ago).count()

    context = {
        'categories': categories,
        'total_categories': total_categories,
        'active_categories': active_categories,
        'inactive_categories': inactive_categories,
        'recent_categories': recent_categories,
    }
    return render(request, 'backend/pages/engins/categories/categorie_list.html', context)


@login_required
def categorie_create(request):
    form = CategorieEnginForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('engins:categorie_list')
    return render(request, 'backend/pages/engins/categories/categorie_form.html', {'form': form})

@login_required
def categorie_update(request, slug):
    obj = get_object_or_404(CategorieEngin, slug=slug)
    form = CategorieEnginForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('engins:categorie_list')
    return render(request, 'backend/pages/engins/categories/categorie_form.html', {'form': form, 'modifier': True})

@login_required
def categorie_delete(request, slug):
    obj = get_object_or_404(CategorieEngin, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('engins:categorie_list')
    return render(request, 'backend/pages/engins/categories/confirm_delete.html', {'obj': obj})

# ===============================
# MARQUES ET MODELES
# ===============================
@login_required
def marque_list(request):
    marques = Marque.objects.all()
    types_engins = TypeEngin.objects.filter(actif=True)

    # Widgets
    total_marques = marques.count()
    active_marques = marques.filter(actif=True).count()
    inactive_marques = marques.filter(actif=False).count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_marques = marques.filter(created_at__gte=thirty_days_ago).count()

    context = {
        'marques': marques,
        'types_engins': types_engins,   # ✅ AJOUT ICI
        'total_marques': total_marques,
        'active_marques': active_marques,
        'inactive_marques': inactive_marques,
        'recent_marques': recent_marques,
    }

    return render(
        request,
        'backend/pages/engins/marques/marque_list.html',
        context
    )

@login_required
def marque_create(request):
    form = MarqueForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('engins:marque_list')
    return render(request, 'backend/pages/engins/marques/form.html', {'form': form})

@login_required
def marque_update(request, slug):
    obj = get_object_or_404(Marque, slug=slug)
    form = MarqueForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('engins:marque_list')
    return render(request, 'backend/pages/engins/marques/form.html', {'form': form, 'modifier': True})

@login_required
def marque_delete(request, slug):
    obj = get_object_or_404(Marque, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('engins:marque_list')
    return render(request, 'backend/pages/engins/marques/confirm_delete.html', {'obj': obj})


# ===============================
# MODELES D'ENGINS
# ===============================
@login_required
def modele_list(request):
    modeles = Modele.objects.all()
    marques = Marque.objects.filter(actif=True)
    types_engins = TypeEngin.objects.filter(actif=True)

    # Widgets statistiques
    total_modeles = modeles.count()
    active_modeles = modeles.filter(actif=True).count()
    inactive_modeles = modeles.filter(actif=False).count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_modeles = modeles.filter(created_at__gte=thirty_days_ago).count()

    context = {
        'modeles': modeles,
        'marques': marques,
        'types_engins': types_engins,
        'total_modeles': total_modeles,
        'active_modeles': active_modeles,
        'inactive_modeles': inactive_modeles,
        'recent_modeles': recent_modeles,
    }
    return render(request, 'backend/pages/engins/modeles/modele_list.html', context)

@login_required
def modele_create(request):
    form = ModeleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('engins:modele_list')
    return render(request, 'backend/pages/engins/modeles/modele_form.html', {'form': form})

@login_required
def modele_update(request, slug):
    obj = get_object_or_404(Modele, slug=slug)
    form = ModeleForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('engins:modele_list')
    return render(request, 'backend/pages/engins/modeles/modele_form.html', {'form': form, 'modifier': True})


@login_required
def modele_delete(request, slug):
    obj = get_object_or_404(Modele, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('engins:modele_list')
    return render(request, 'backend/pages/engins/modeles/confirm_delete.html', {'obj': obj})

# ===============================
# STATUTS ENGINS
# ===============================
@login_required
def statut_list(request):
    statuts = StatutEngin.objects.all()

    total_statuts = statuts.count()
    active_statuts = statuts.filter(actif=True).count()
    inactive_statuts = statuts.filter(actif=False).count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_statuts = statuts.filter(created_at__gte=thirty_days_ago).count()

    context = {
        'statuts': statuts,
        'total_statuts': total_statuts,
        'active_statuts': active_statuts,
        'inactive_statuts': inactive_statuts,
        'recent_statuts': recent_statuts,
    }
    return render(request, 'backend/pages/engins/statuts/statut_list.html', context)

@login_required
def statut_create(request):
    form = StatutEnginForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('engins:statut_list')
    return render(request, 'backend/pages/engins/statuts/form.html', {'form': form})

@login_required
def statut_update(request, slug):
    obj = get_object_or_404(StatutEngin, slug=slug)
    form = StatutEnginForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('engins:statut_list')
    return render(request, 'backend/pages/engins/statuts/form.html', {'form': form, 'modifier': True})

@login_required
def statut_delete(request, slug):
    obj = get_object_or_404(StatutEngin, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('engins:statut_list')
    return render(request, 'backend/pages/engins/statuts/confirm_delete.html', {'obj': obj})


# ===============================
# SITES / DEPOTS
# ===============================
@login_required
def site_list(request):
    sites = SiteEngin.objects.all()

    total_sites = sites.count()
    active_sites = sites.filter(actif=True).count()
    inactive_sites = sites.filter(actif=False).count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_sites = sites.filter(created_at__gte=thirty_days_ago).count()

    context = {
        'sites': sites,
        'total_sites': total_sites,
        'active_sites': active_sites,
        'inactive_sites': inactive_sites,
        'recent_sites': recent_sites,
    }
    return render(request, 'backend/pages/engins/sites/site_list.html', context)

@login_required
def site_create(request):
    form = SiteEnginForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('engins:site_list')
    return render(request, 'backend/pages/engins/sites/site_form.html', {'form': form})

@login_required
def site_update(request, slug):
    obj = get_object_or_404(SiteEngin, slug=slug)
    form = SiteEnginForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('engins:site_list')
    return render(request, 'backend/pages/engins/sites/site_form.html', {'form': form, 'modifier': True})

@login_required
def site_delete(request, slug):
    obj = get_object_or_404(SiteEngin, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('engins:site_list')
    return render(request, 'backend/pages/engins/sites/confirm_delete.html', {'obj': obj})

# ===============================
# ENGINS
# ===============================
@login_required
def engin_list(request):
    engins = Engin.objects.all()

    total_engins = engins.count()
    active_engins = engins.filter(actif=True).count()
    inactive_engins = engins.filter(actif=False).count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_engins = engins.filter(created_at__gte=thirty_days_ago).count()

    context = {
        'engins': engins,
        'total_engins': total_engins,
        'active_engins': active_engins,
        'inactive_engins': inactive_engins,
        'recent_engins': recent_engins,
    }
    return render(request, 'backend/pages/engins/engins/engin_list.html', context)

@login_required
def engin_create(request):
    if request.method == 'POST':
        form = EnginForm(request.POST)
        remorque_form = RemorqueForm(request.POST, prefix="remorque")
        citerne_form = CiterneForm(request.POST, prefix="citerne")

        # 📎 Documents Engin
        fichier_form = FichierJointForm(
            request.POST, request.FILES,
            prefix="fichier",
            module="engin"
        )

        # 📎 Documents Remorque
        remorque_fichier_form = FichierJointForm(
            request.POST, request.FILES,
            prefix="remorque_docs",
            module="remorque"
        )

        # 📎 Documents Citerne
        citerne_documents_form = FichierJointForm(
            request.POST, request.FILES,
            prefix="citerne_docs",
            module="citerne"
        )

        if form.is_valid():
            engin = form.save()
            type_nom = engin.type_engin.nom.lower()

            # 🚛 CITERNE
            if "citerne" in type_nom and citerne_form.is_valid():
                citerne = citerne_form.save(commit=False)
                citerne.engin = engin
                citerne.actif = True
                citerne.save()

                if citerne_documents_form.is_valid():
                    doc = citerne_documents_form.save(commit=False)
                    doc.content_object = citerne
                    doc.save()

            # 🚚 REMORQUE / TRACTEUR
            if ("tracteur" in type_nom or "remorque" in type_nom) and remorque_form.is_valid():
                remorque = remorque_form.save(commit=False)
                remorque.engin = engin
                remorque.actif = True
                remorque.save()

                if remorque_fichier_form.is_valid():
                    doc = remorque_fichier_form.save(commit=False)
                    doc.content_object = remorque
                    doc.save()

            # 📎 DOCUMENT ENGINS
            if fichier_form.is_valid():
                fichier = fichier_form.save(commit=False)
                fichier.content_object = engin
                fichier.save()

            return redirect('engins:engin_list')

    else:
        form = EnginForm()
        remorque_form = RemorqueForm(prefix="remorque")
        citerne_form = CiterneForm(prefix="citerne")

        fichier_form = FichierJointForm(prefix="fichier", module="engin")
        remorque_fichier_form = FichierJointForm(prefix="remorque_docs", module="remorque")
        citerne_documents_form = FichierJointForm(prefix="citerne_docs", module="citerne")

    return render(request, 'backend/pages/engins/engins/engin_form.html', {
        'form': form,
        'remorque_form': remorque_form,
        'citerne_form': citerne_form,
        'fichier_form': fichier_form,
        'remorque_fichier_form': remorque_fichier_form,
        'citerne_documents_form': citerne_documents_form,
    })

@login_required
def engin_update(request, slug):
    engin = get_object_or_404(Engin, slug=slug)

    remorque_instance = getattr(engin, 'remorque', None)
    citerne_instance = getattr(engin, 'citerne', None)

    if request.method == 'POST':
        form = EnginForm(request.POST, instance=engin)
        remorque_form = RemorqueForm(request.POST, instance=remorque_instance, prefix="remorque")
        citerne_form = CiterneForm(request.POST, instance=citerne_instance, prefix="citerne")

        fichier_form = FichierJointForm(
            request.POST, request.FILES,
            prefix="fichier",
            module="engin"
        )

        remorque_fichier_form = FichierJointForm(
            request.POST, request.FILES,
            prefix="remorque_docs",
            module="remorque"
        )

        citerne_documents_form = FichierJointForm(
            request.POST, request.FILES,
            prefix="citerne_docs",
            module="citerne"
        )

        if form.is_valid():
            engin = form.save()
            type_nom = engin.type_engin.nom.lower()

            # 🚛 CITERNE
            if "citerne" in type_nom and citerne_form.is_valid():
                citerne = citerne_form.save(commit=False)
                citerne.engin = engin
                citerne.actif = True
                citerne.save()

                if citerne_documents_form.is_valid():
                    doc = citerne_documents_form.save(commit=False)
                    doc.content_object = citerne
                    doc.save()
            else:
                Citerne.objects.filter(engin=engin).update(actif=False)

            # 🚚 REMORQUE / TRACTEUR
            if ("tracteur" in type_nom or "remorque" in type_nom) and remorque_form.is_valid():
                remorque = remorque_form.save(commit=False)
                remorque.engin = engin
                remorque.actif = True
                remorque.save()

                if remorque_fichier_form.is_valid():
                    doc = remorque_fichier_form.save(commit=False)
                    doc.content_object = remorque
                    doc.save()

            # 📎 DOCUMENT ENGINS
            if fichier_form.is_valid():
                fichier = fichier_form.save(commit=False)
                fichier.content_object = engin
                fichier.save()

            return redirect('engins:engin_list')

    else:
        form = EnginForm(instance=engin)
        remorque_form = RemorqueForm(instance=remorque_instance, prefix="remorque")
        citerne_form = CiterneForm(instance=citerne_instance, prefix="citerne")

        fichier_form = FichierJointForm(prefix="fichier", module="engin")
        remorque_fichier_form = FichierJointForm(prefix="remorque_docs", module="remorque")
        citerne_documents_form = FichierJointForm(prefix="citerne_docs", module="citerne")

    return render(request, 'backend/pages/engins/engins/engin_form.html', {
        'form': form,
        'remorque_form': remorque_form,
        'citerne_form': citerne_form,
        'fichier_form': fichier_form,
        'remorque_fichier_form': remorque_fichier_form,
        'citerne_documents_form': citerne_documents_form,
        'modifier': True
    })

@login_required
def engin_delete(request, slug):
    obj = get_object_or_404(Engin, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('engins:engin_list')
    return render(request, 'backend/pages/engins/engins/confirm_delete.html', {'obj': obj})

# ===============================
# DASHBOARD ENGINS
# ===============================
@login_required
def dashboard_engins(request):
    engins = Engin.objects.all()

    total_engins = engins.count()
    active_engins = engins.filter(actif=True).count()
    inactive_engins = engins.filter(actif=False).count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_engins = engins.filter(created_at__gte=thirty_days_ago).count()

    types_count = TypeEngin.objects.count()
    categories_count = CategorieEngin.objects.count()
    marques_count = Marque.objects.count()
    statuts_count = StatutEngin.objects.count()
    sites_count = SiteEngin.objects.count()

    context = {
        'total_engins': total_engins,
        'active_engins': active_engins,
        'inactive_engins': inactive_engins,
        'recent_engins': recent_engins,
        'types_count': types_count,
        'categories_count': categories_count,
        'marques_count': marques_count,
        'statuts_count': statuts_count,
        'sites_count': sites_count,
    }
    return render(request, 'backend/pages/engins/dashboard_engins/dashboard_engins.html', context)

