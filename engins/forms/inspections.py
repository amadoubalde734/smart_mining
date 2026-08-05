
from django import forms
from engins.models import (
    InspectionEngin, SignalisationInspection, ExterieurInspection,
    EPIInspection, MoteurInspection, FreinageInspection,
    PartiesMobilesInspection, PneumatiquesInspection,
    MecanismesInspection, ETAT_PF_MD, ETAT_OK_NON
)
from django import forms
from engins.models import InspectionEngin, ETAT_PF_MD, ETAT_OK_NON, FUITES_CHOICES, DECISION_CHOICES, PARTIE_CHOICES


# =========================================================
# CHAMP CHECKBOX À CHOIX UNIQUE (pf/md ou ok/non ou autres)
# =========================================================
class SingleCheckboxChoiceField(forms.MultipleChoiceField):
    """
    Affiche des checkboxes mais force UNE seule valeur
    """
    def clean(self, value):
        value = super().clean(value)
        if not value or len(value) != 1:
            raise forms.ValidationError("Veuillez cocher une seule case.")
        return value[0]  # retourne une seule valeur

# =========================
# FACTORIES POUR LES CHECKBOXES
# =========================
def pf_md_checkbox():
    return SingleCheckboxChoiceField(
        choices=ETAT_PF_MD,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

def ok_non_checkbox():
    return SingleCheckboxChoiceField(
        choices=ETAT_OK_NON,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

def fuite_checkbox():
    return SingleCheckboxChoiceField(
        choices=FUITES_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

def decision_checkbox():
    return SingleCheckboxChoiceField(
        choices=DECISION_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

# =========================================================
# FORMULAIRE PRINCIPAL INSPECTION
# =========================================================
class InspectionEnginForm(forms.ModelForm):

    # DOCUMENTS
    carte_grise_tracteur = ok_non_checkbox()
    carte_grise_remorque = ok_non_checkbox()
    assurance_tracteur = ok_non_checkbox()
    assurance_remorque = ok_non_checkbox()
    visite_technique_tracteur = ok_non_checkbox()
    visite_technique_remorque = ok_non_checkbox()
    permis_conduire = ok_non_checkbox()

    # FUITES
    fuite_huile_moteur = fuite_checkbox()
    fuite_hydraulique = fuite_checkbox()
    fuite_carburant = fuite_checkbox()

    # DECISION FINALE
    decision_finale = decision_checkbox()

    class Meta:
        model = InspectionEngin
        fields = [
            'partie', 'engin', 'remorque', 'type_engin',
            'date_inspection', 'numero_inspection',
            'chauffeur', 'responsable', 'kilometrage',
            'pass_mine', 'telephone', 'flotte',
            'dernier_chiffre_chassis',

            'carte_grise_tracteur', 'carte_grise_remorque',
            'assurance_tracteur', 'assurance_remorque',
            'visite_technique_tracteur', 'visite_technique_remorque',
            'permis_conduire',

            'fuite_huile_moteur', 'fuite_hydraulique', 'fuite_carburant',
            'decision_finale', 'observations'
        ]

        widgets = {
            'partie': forms.Select(attrs={'class': 'form-select'}),
            'engin': forms.Select(attrs={'class': 'form-select'}),
            'remorque': forms.Select(attrs={'class': 'form-select'}),
            'type_engin': forms.Select(attrs={'class': 'form-select'}),
            'date_inspection': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_inspection': forms.TextInput(attrs={'class': 'form-control'}),
            'chauffeur': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'kilometrage': forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_mine': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'flotte': forms.TextInput(attrs={'class': 'form-control'}),
            'dernier_chiffre_chassis': forms.TextInput(attrs={'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        partie = cleaned_data.get('partie')

        if partie == 'tracteur' and not cleaned_data.get('engin'):
            raise forms.ValidationError("Pour un tracteur, l'engin est obligatoire.")
        if partie == 'remorque' and not cleaned_data.get('remorque'):
            raise forms.ValidationError("Pour une remorque, la remorque est obligatoire.")

        return cleaned_data

# =========================================================
# FORMULAIRES PF / MD
# =========================================================
class SignalisationInspectionForm(forms.ModelForm):
    phares_led = pf_md_checkbox()
    orientation_phares = pf_md_checkbox()
    feux_position_avant = pf_md_checkbox()
    feux_stop_arriere = pf_md_checkbox()
    feux_direction = pf_md_checkbox()
    klaxon = pf_md_checkbox()
    gyrophare = pf_md_checkbox()
    lumieres_plaques = pf_md_checkbox()

    class Meta:
        model = SignalisationInspection
        exclude = ['inspection']


class ExterieurInspectionForm(forms.ModelForm):
    pare_brise = pf_md_checkbox()
    retroviseurs = pf_md_checkbox()
    glaces_balais = pf_md_checkbox()
    garde_boue = pf_md_checkbox()
    ridelles_bennes = pf_md_checkbox()
    integrite_citerne = pf_md_checkbox()
    sieges_fixes = pf_md_checkbox()
    sorties_secours = pf_md_checkbox()
    volant = pf_md_checkbox()
    climatisation = pf_md_checkbox()

    class Meta:
        model = ExterieurInspection
        exclude = ['inspection']


class EPIInspectionForm(forms.ModelForm):
    extincteur_abc_2_9kg = pf_md_checkbox()
    extincteur_abc_6kg = pf_md_checkbox()
    trousse_pharmacie = pf_md_checkbox()
    cric_hydraulique = pf_md_checkbox()
    ceinture_securite = pf_md_checkbox()
    cle_roues = pf_md_checkbox()
    triangle_signalisation = pf_md_checkbox()
    casque_protection = pf_md_checkbox()
    lampe_torche = pf_md_checkbox()
    gilet_hv = pf_md_checkbox()
    masque_antipoussiere = pf_md_checkbox()
    ruban_balisage = pf_md_checkbox()
    gants_manutention = pf_md_checkbox()
    cales_roues = pf_md_checkbox()
    chaussures_securite = pf_md_checkbox()
    alarme_recul = pf_md_checkbox()

    class Meta:
        model = EPIInspection
        exclude = ['inspection']


class MoteurInspectionForm(forms.ModelForm):
    manometre_air = pf_md_checkbox()
    decharge_regulateur = pf_md_checkbox()
    organes_freinage = pf_md_checkbox()
    temps_remplissage_bouteilles = pf_md_checkbox()
    pression_decharge = pf_md_checkbox()
    pression_demarrage_compresseur = pf_md_checkbox()

    class Meta:
        model = MoteurInspection
        exclude = ['inspection']


class FreinageInspectionForm(forms.ModelForm):
    fuite_air = pf_md_checkbox()
    controle_tuyaux_air = pf_md_checkbox()
    circuit_electrique = pf_md_checkbox()
    circuit_pneumatique_1 = pf_md_checkbox()
    circuit_pneumatique_2 = pf_md_checkbox()
    correcteur_freinage = pf_md_checkbox()
    feux_freinage = pf_md_checkbox()

    class Meta:
        model = FreinageInspection
        exclude = ['inspection']


class MecanismesInspectionForm(forms.ModelForm):
    reservoir_carburant = pf_md_checkbox()
    boucle_accrochement = pf_md_checkbox()
    support_roue_secours = pf_md_checkbox()
    systeme_frein_remorque = pf_md_checkbox()
    circuit_hydraulique = pf_md_checkbox()

    class Meta:
        model = MecanismesInspection
        exclude = ['inspection']


class PartiesMobilesInspectionForm(forms.ModelForm):
    reservoir_carburant = pf_md_checkbox()
    barre_accouplement = pf_md_checkbox()
    boucle_accrochage = pf_md_checkbox()
    support_roue_secours = pf_md_checkbox()
    systeme_frein_remorque = pf_md_checkbox()
    circuit_hydraulique = pf_md_checkbox()
    felures_chassis_remorque = pf_md_checkbox()
    porte_benne = pf_md_checkbox()
    fermeture_benne = pf_md_checkbox()
    bagues_direction = pf_md_checkbox()
    rotules_direction = pf_md_checkbox()
    sommier_sellette = pf_md_checkbox()
    sellette_plate = pf_md_checkbox()

    class Meta:
        model = PartiesMobilesInspection
        exclude = ['inspection', 'citerne']


class PneumatiquesInspectionForm(forms.ModelForm):
    pneus_avant = pf_md_checkbox()
    pneus_arriere = pf_md_checkbox()
    pression_pneus = pf_md_checkbox()
    usure_pneus = pf_md_checkbox()
    ecrous_roues = pf_md_checkbox()
    jantes = pf_md_checkbox()
    roue_secours = pf_md_checkbox()

    class Meta:
        model = PneumatiquesInspection
        exclude = ['inspection']

