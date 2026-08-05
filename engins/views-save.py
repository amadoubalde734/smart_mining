from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from django.contrib import messages
from .models import  SiteEngin, Engin, AssuranceEngin, VignetteConformite, ControleTechnique
from .forms import  AssuranceEnginForm
# =========================
# MODELS
# =========================
from .models import (
    Engin, TypeEngin, CategorieEngin, Marque,Modele, 
    StatutEngin, SiteEngin, Citerne, InspectionEngin,CertificatJaugeage
)

# =========================
# FORMS
# =========================
from .forms import (
    # --- Paramétrage engins ---
    TypeEnginForm,
    CategorieEnginForm,
    MarqueForm,
    ModeleForm,
    StatutEnginForm,
    SiteEnginForm,
    EnginForm,
    RemorqueForm, 
    CiterneForm,

    # --- Inspection engins ---
    InspectionEnginForm,
    SignalisationInspectionForm,
    ExterieurInspectionForm,
    EPIInspectionForm,
    MoteurInspectionForm,
    FreinageInspectionForm,
    PartiesMobilesInspectionForm,
    MecanismesInspectionForm,
    PneumatiquesInspectionForm,
    
)

# =========================
# FORMS DOCUMENTS
# =========================
from documents.forms import FichierJointForm
from .forms import CertificatJaugeageForm, CertificatJaugeageDocumentForm
# ===============================
# TYPES D'ENGINS
# ===============================

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
from django.utils import timezone
from datetime import timedelta

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
from django.utils import timezone
from datetime import timedelta
from .models import Marque, TypeEngin

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
from django.utils import timezone
from datetime import timedelta
from .models import Modele, Marque, TypeEngin
from .forms import ModeleForm

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
# CRÉATION D'UNE INSPECTION ENGINS
# ===============================
@login_required
def inspection_create(request):
    if request.method == "POST":
        inspection_form = InspectionEnginForm(request.POST)
        signalisation_form = SignalisationInspectionForm(request.POST)
        exterieur_form = ExterieurInspectionForm(request.POST)
        epi_form = EPIInspectionForm(request.POST)
        moteur_form = MoteurInspectionForm(request.POST)
        freinage_form = FreinageInspectionForm(request.POST)
        parties_mobiles_form = PartiesMobilesInspectionForm(request.POST)
        pneumatiques_form = PneumatiquesInspectionForm(request.POST)
        mecanismes_form = MecanismesInspectionForm(request.POST)
        extincteur_form = EPIInspectionForm(request.POST)  # ou formulaire spécifique aux extincteurs

        forms_list = [
            inspection_form, signalisation_form, exterieur_form, epi_form,
            moteur_form, freinage_form, parties_mobiles_form, pneumatiques_form,
            mecanismes_form, extincteur_form
        ]

        if all(f.is_valid() for f in forms_list):
            inspection = inspection_form.save()
            for form in [
                signalisation_form, exterieur_form, epi_form, moteur_form,
                freinage_form, parties_mobiles_form, pneumatiques_form,
                mecanismes_form, extincteur_form
            ]:
                obj = form.save(commit=False)
                obj.inspection = inspection
                obj.save()

            messages.success(request, "Inspection enregistrée avec succès !")
            return redirect('inspections:inspection_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        inspection_form = InspectionEnginForm()
        signalisation_form = SignalisationInspectionForm()
        exterieur_form = ExterieurInspectionForm()
        epi_form = EPIInspectionForm()
        moteur_form = MoteurInspectionForm()
        freinage_form = FreinageInspectionForm()
        parties_mobiles_form = PartiesMobilesInspectionForm()
        pneumatiques_form = PneumatiquesInspectionForm()
        mecanismes_form = MecanismesInspectionForm()
        extincteur_form = EPIInspectionForm()  # ou formulaire spécifique aux extincteurs

    # --------------------
    # Préparer champs EPI (2 colonnes)
    epi_fields = [
        ("trousse_pharmacie", epi_form["trousse_pharmacie"]),
        ("cric_hydraulique", epi_form["cric_hydraulique"]),
        ("ceinture_securite", epi_form["ceinture_securite"]),
        ("cle_roues", epi_form["cle_roues"]),
        ("triangle_signalisation", epi_form["triangle_signalisation"]),
        ("casque_protection", epi_form["casque_protection"]),
        ("lampe_torche", epi_form["lampe_torche"]),
        ("gilet_hv", epi_form["gilet_hv"]),
        ("masque_antipoussiere", epi_form["masque_antipoussiere"]),
        ("ruban_balisage", epi_form["ruban_balisage"]),
        ("gants_manutention", epi_form["gants_manutention"]),
        ("cales_roues", epi_form["cales_roues"]),
        ("chaussures_securite", epi_form["chaussures_securite"]),
        ("alarme_recul", epi_form["alarme_recul"]),
    ]
    mid_index_epi = len(epi_fields) // 2
    epi_fields_left = epi_fields[:mid_index_epi]
    epi_fields_right = epi_fields[mid_index_epi:]

    # --------------------
    # Préparer champs Parties Mobiles (2 colonnes)
    parties_mobiles_field_names = list(parties_mobiles_form.fields.keys())
    mid_index_pm = len(parties_mobiles_field_names) // 2
    parties_mobiles_left = [(name, parties_mobiles_form[name]) for name in parties_mobiles_field_names[:mid_index_pm]]
    parties_mobiles_right = [(name, parties_mobiles_form[name]) for name in parties_mobiles_field_names[mid_index_pm:]]

    # --------------------
    # Préparer champs Extincteurs (2 colonnes)
    extincteur_field_names = list(extincteur_form.fields.keys())
    mid_index_extincteur = len(extincteur_field_names) // 2
    extincteur_fields_left = [(name, extincteur_form[name]) for name in extincteur_field_names[:mid_index_extincteur]]
    extincteur_fields_right = [(name, extincteur_form[name]) for name in extincteur_field_names[mid_index_extincteur:]]

    # --------------------
    # Préparer champs Fuites (3 colonnes)
    fuite_fields = [
        ("fuite_huile_moteur", inspection_form["fuite_huile_moteur"]),
        ("fuite_hydraulique", inspection_form["fuite_hydraulique"]),
        ("fuite_carburant", inspection_form["fuite_carburant"]),
    ]
    fuite_left = [fuite_fields[0]]
    fuite_middle = [fuite_fields[1]]
    fuite_right = [fuite_fields[2]]

    context = {
        'form': inspection_form,
        'signalisation_form': signalisation_form,
        'exterieur_form': exterieur_form,
        'epi_form': epi_form,
        'epi_fields_left': epi_fields_left,
        'epi_fields_right': epi_fields_right,
        'moteur_form': moteur_form,
        'freinage_form': freinage_form,
        'parties_mobiles_form': parties_mobiles_form,
        'parties_mobiles_left': parties_mobiles_left,
        'parties_mobiles_right': parties_mobiles_right,
        'pneumatiques_form': pneumatiques_form,
        'mecanismes_form': mecanismes_form,
        'extincteur_form': extincteur_form,
        'extincteur_fields_left': extincteur_fields_left,
        'extincteur_fields_right': extincteur_fields_right,
        'fuite_left': fuite_left,
        'fuite_middle': fuite_middle,
        'fuite_right': fuite_right,
        'decision_finale': inspection_form["decision_finale"],
        'engins': Engin.objects.all(),
    }

    return render(request, 'backend/pages/engins/inspections/inspection_engin_form.html', context)

# ===============================
# LISTE DES INSPECTIONS ENGINS
@login_required
def inspection_list(request):
    inspections = InspectionEngin.objects.all().order_by('-date_inspection')
    
    # Statistiques
    total_inspections = inspections.count()
    active_inspections = inspections.filter(decision_finale='apte').count()
    inactive_inspections = inspections.filter(decision_finale='non_apte').count()
    recent_inspections = inspections.filter(date_inspection__gte=timezone.now()-timedelta(days=30)).count()
    
    # Pagination
    paginator = Paginator(inspections, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_inspections': total_inspections,
        'active_inspections': active_inspections,
        'inactive_inspections': inactive_inspections,
        'recent_inspections': recent_inspections,
    }
    return render(request, 'backend/pages/engins/inspections/inspection_list.html', context)

#   ==============================
# MODIFICATION D'UNE INSPECTION
@login_required
def inspection_update(request, slug):
    inspection = get_object_or_404(InspectionEngin, slug=slug)

    if request.method == "POST":
        inspection_form = InspectionEnginForm(request.POST, instance=inspection)
        signalisation_form = SignalisationInspectionForm(request.POST, instance=getattr(inspection, 'signalisation', None))
        exterieur_form = ExterieurInspectionForm(request.POST, instance=getattr(inspection, 'exterieur', None))
        epi_form = EPIInspectionForm(request.POST, instance=getattr(inspection, 'epi', None))
        moteur_form = MoteurInspectionForm(request.POST, instance=getattr(inspection, 'moteur', None))
        freinage_form = FreinageInspectionForm(request.POST, instance=getattr(inspection, 'freinage', None))
        parties_mobiles_form = PartiesMobilesInspectionForm(request.POST, instance=getattr(inspection, 'parties_mobiles', None))

        if (inspection_form.is_valid() and
            signalisation_form.is_valid() and
            exterieur_form.is_valid() and
            epi_form.is_valid() and
            moteur_form.is_valid() and
            freinage_form.is_valid() and
            parties_mobiles_form.is_valid()):

            inspection_form.save()
            signalisation_form.save()
            exterieur_form.save()
            epi_form.save()
            moteur_form.save()
            freinage_form.save()
            parties_mobiles_form.save()

            messages.success(request, "Inspection mise à jour avec succès !")
            return redirect('inspections:inspection_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        inspection_form = InspectionEnginForm(instance=inspection)
        signalisation_form = SignalisationInspectionForm(instance=getattr(inspection, 'signalisation', None))
        exterieur_form = ExterieurInspectionForm(instance=getattr(inspection, 'exterieur', None))
        epi_form = EPIInspectionForm(instance=getattr(inspection, 'epi', None))
        moteur_form = MoteurInspectionForm(instance=getattr(inspection, 'moteur', None))
        freinage_form = FreinageInspectionForm(instance=getattr(inspection, 'freinage', None))
        parties_mobiles_form = PartiesMobilesInspectionForm(instance=getattr(inspection, 'parties_mobiles', None))

    context = {
        'form': inspection_form,
        'signalisation_form': signalisation_form,
        'exterieur_form': exterieur_form,
        'epi_form': epi_form,
        'moteur_form': moteur_form,
        'freinage_form': freinage_form,
        'parties_mobiles_form': parties_mobiles_form,
    }
    return render(request, 'backend/pages/engins/inspections/inspection_engin_form.html', context)

# ===============================
# DÉTAIL D'UNE INSPECTION
@login_required
def inspection_detail(request, slug):
    inspection = get_object_or_404(InspectionEngin, slug=slug)
    
    context = {
        'inspection': inspection,
    }
    return render(request, 'inspections/inspection_detail.html', context)

# ===============================
# SUPPRESSION D'UNE INSPECTION

def inspection_delete(request, slug):
    inspection = get_object_or_404(InspectionEngin, slug=slug)
    
    if request.method == "POST":
        inspection.delete()
        messages.success(request, "Inspection supprimée avec succès !")
        return redirect('inspections:inspection_list')
    
    context = {
        'inspection': inspection,
    }
    return render(request, 'inspections/inspection_confirm_delete.html', context)


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
# VIGNETTES
# ===============================
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

from .models import VignetteConformite, Engin

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
# CONTROLES TECHNIQUES
# ===============================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ControleTechnique
from .forms import ControleTechniqueForm
from .forms import ControleTechniqueForm, ControleTechniqueDocumentForm

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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

# ===============================
# PAGE DOCUMENTS LÉGAUX
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


# ===============================
# LISTE DES CERTIFICATS DE JAUGEAGE
# ===============================
def certificat_jaugeage_list(request):
    certificats = CertificatJaugeage.objects.select_related('engin').all()

    total_certificats = certificats.count()
    valid_certificats = certificats.filter(en_validite=True).count()  # nécessite le champ en_validite
    expired_certificats = certificats.filter(en_validite=False).count()

    context = {
        'certificats': certificats,
        'total_certificats': total_certificats,
        'valid_certificats': valid_certificats,
        'expired_certificats': expired_certificats,
    }
    return render(request, 'backend/pages/engins/engins/certificat_jaugeage_list.html', context)

# ===============================
# AJOUT D'UN CERTIFICAT DE JAUGEAGE
# ===============================
def certificat_jaugeage_create(request):
    if request.method == "POST":
        form = CertificatJaugeageForm(request.POST, request.FILES)
        doc_form = CertificatJaugeageDocumentForm(request.POST, request.FILES)  # utilisation correcte
        if form.is_valid() and doc_form.is_valid():
            certificat = form.save()
            doc = doc_form.save(commit=False)
            doc.content_object = certificat
            doc.save()
            messages.success(request, "Certificat de jaugeage ajouté avec succès.")
            return redirect("engins:documents_legaux")
        else:
            messages.error(request, "Erreur lors de l'ajout du certificat.")
    else:
        form = CertificatJaugeageForm()
        doc_form = CertificatJaugeageDocumentForm()  # utilisation correcte

    return render(request, "backend/pages/engins/engins/certificat_jaugeage_create.html", {
        "form": form,
        "doc_form": doc_form,
    })

# ===============================
# MISE À JOUR D'UN CERTIFICAT DE JAUGEAGE
# ===============================
def certificat_jaugeage_update(request, pk):
    certificat = get_object_or_404(CertificatJaugeage, pk=pk)

    if request.method == "POST":
        form = CertificatJaugeageForm(request.POST, request.FILES, instance=certificat)
        doc_form = CertificatJaugeageDocumentForm(request.POST, request.FILES)  # utilisation correcte
        if form.is_valid() and doc_form.is_valid():
            form.save()
            doc = doc_form.save(commit=False)
            doc.content_object = certificat
            doc.save()
            messages.success(request, "Certificat modifié avec succès.")
            return redirect("engins:documents_legaux")
        else:
            messages.error(request, "Erreur lors de la modification du certificat.")
    else:
        form = CertificatJaugeageForm(instance=certificat)
        doc_form = CertificatJaugeageDocumentForm()  # utilisation correcte

    return render(request, "backend/pages/engins/engins/certificat_jaugeage_update.html", {
        "form": form,
        "doc_form": doc_form,
        "certificat": certificat,
    })

# ===============================
# SUPPRESSION D'UN CERTIFICAT DE JAUGEAGE
# ===============================
def certificat_jaugeage_delete(request, pk):
    certificat = get_object_or_404(CertificatJaugeage, pk=pk)
    if request.method == "POST":
        certificat.delete()
        messages.success(request, "Certificat de jaugeage supprimé avec succès.")
        return redirect("engins:documents_legaux")

    return render(request, "backend/pages/engins/engins/certificat_jaugeage_delete.html", {
        "certificat": certificat
    })
#
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
