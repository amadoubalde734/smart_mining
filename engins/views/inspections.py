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
    InspectionEngin,
)

# =========================
# FORMS - Inspections Engins
# =========================
from ..forms import (
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

