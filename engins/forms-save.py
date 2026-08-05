from django import forms
from .models import (
    TypeEngin,
    CategorieEngin,
    Marque,
    Modele,
    StatutEngin,
    SiteEngin,
    Engin,
    Remorque,
    Citerne,
    InspectionEngin,
    SignalisationInspection,
    ExterieurInspection,
    EPIInspection,
    MoteurInspection,
    FreinageInspection,
    PartiesMobilesInspection,
    CertificatJaugeage,
)
from personnel.models import Employe
from documents.forms import FichierJointForm

# ===============================
# TYPES D'ENGINS
# ===============================
class TypeEnginForm(forms.ModelForm):
    class Meta:
        model = TypeEngin
        fields = ['nom', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom du type d'engin"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===============================
# CATEGORIES D'ENGINS
# ===============================
class CategorieEnginForm(forms.ModelForm):
    class Meta:
        model = CategorieEngin
        fields = ['nom', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===============================
# MARQUES
# ===============================
class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        fields = ['nom', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la marque'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===============================
# MODELES
# ===============================
class ModeleForm(forms.ModelForm):
    class Meta:
        model = Modele
        fields = ['marque', 'nom', 'type_engin', 'actif']
        widgets = {
            'marque': forms.Select(attrs={'class': 'form-select'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du modèle'}),
            'type_engin': forms.Select(attrs={'class': 'form-select'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===============================
# STATUTS ENGINS
# ===============================
class StatutEnginForm(forms.ModelForm):
    class Meta:
        model = StatutEngin
        fields = ['nom', 'description', 'actif']
        widgets = {
            'nom': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description du statut'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===============================
# SITES / DEPOTS
# ===============================
class SiteEnginForm(forms.ModelForm):
    class Meta:
        model = SiteEngin
        fields = ['nom_site', 'adresse', 'description', 'actif']
        widgets = {
            'nom_site': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du site'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse du site'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===============================   
class EnginForm(forms.ModelForm):
    class Meta:
        model = Engin
        fields = [
            'immatriculation', 'marque', 'modele', 'type_engin', 'categorie',
            'statut', 'site', 'couleur', 'numero_chassis',
            'date_mise_circulation', 'date_integration_ums',
            'proprietaire', 'contact_proprietaire', 'type_chassis',
            'nombre_essieux', 'volume_benne_citerne',
            'type_fermeture_benne', 'commentaire',
            'camion_communautaire', 'actif',
        ]

        widgets = {
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'marque': forms.Select(attrs={'class': 'form-select'}),
            'modele': forms.Select(attrs={'class': 'form-select'}),
            'type_engin': forms.Select(attrs={'class': 'form-select'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'site': forms.Select(attrs={'class': 'form-select'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_chassis': forms.TextInput(attrs={'class': 'form-control'}),
            'date_mise_circulation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_integration_ums': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proprietaire': forms.Select(attrs={'class': 'form-select'}),
            'contact_proprietaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_chassis': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_essieux': forms.NumberInput(attrs={'class': 'form-control'}),
            'volume_benne_citerne': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_fermeture_benne': forms.TextInput(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'camion_communautaire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrage des modèles selon le type d'engin sélectionné
        if 'type_engin' in self.data:
            try:
                type_id = int(self.data.get('type_engin'))
                self.fields['modele'].queryset = Modele.objects.filter(type_engin_id=type_id)
            except (ValueError, TypeError):
                self.fields['modele'].queryset = Modele.objects.none()
        elif self.instance.pk and self.instance.type_engin:
            self.fields['modele'].queryset = Modele.objects.filter(type_engin=self.instance.type_engin)

    def clean(self):
        cleaned_data = super().clean()
        type_engin = cleaned_data.get('type_engin')
        volume = cleaned_data.get('volume_benne_citerne')
        proprietaire = cleaned_data.get('proprietaire')
        communautaire = cleaned_data.get('camion_communautaire')

        if not type_engin:
            raise forms.ValidationError("Le type d'engin est obligatoire.")

        nom_type = type_engin.nom.lower()

        if ("citerne" in nom_type or "benne" in nom_type) and not volume:
            raise forms.ValidationError(
                "Le volume benne / citerne est obligatoire pour ce type d'engin."
            )

        if not communautaire and not proprietaire:
            raise forms.ValidationError(
                "Le propriétaire est obligatoire si l'engin n'est pas communautaire."
            )

        return cleaned_data

class RemorqueForm(forms.ModelForm):
    class Meta:
        model = Remorque
        fields = [
            'immatriculation', 'numero_chassis', 'marque', 'modele',
            'couleur', 'volume_benne_citerne', 'type_remorque',
            'tracteur', 'actif',
        ]

        widgets = {
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_chassis': forms.TextInput(attrs={'class': 'form-control'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'modele': forms.TextInput(attrs={'class': 'form-control'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control'}),
            'volume_benne_citerne': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_remorque': forms.Select(attrs={'class': 'form-select'}),
            'tracteur': forms.Select(attrs={'class': 'form-select'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
   
class CiterneForm(forms.ModelForm):
    class Meta:
        model = Citerne
        fields = ['numero_serie', 'volume', 'type_fermeture', 'engin', 'remorque', 'actif']

        widgets = {
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_fermeture': forms.TextInput(attrs={'class': 'form-control'}),
            'engin': forms.Select(attrs={'class': 'form-select'}),
            'remorque': forms.Select(attrs={'class': 'form-select'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        engin = cleaned_data.get('engin')
        remorque = cleaned_data.get('remorque')

        if not engin and not remorque:
            raise forms.ValidationError(
                "Vous devez sélectionner soit un Engin soit une Remorque."
            )

        if engin and remorque:
            raise forms.ValidationError(
                "Une citerne ne peut être liée qu'à un Engin ou une Remorque."
            )

        return cleaned_data

from django import forms
from .models import (
    InspectionEngin, SignalisationInspection, ExterieurInspection,
    EPIInspection, MoteurInspection, FreinageInspection,
    PartiesMobilesInspection, PneumatiquesInspection,
    MecanismesInspection, ETAT_PF_MD, ETAT_OK_NON
)
from django import forms
from .models import InspectionEngin, ETAT_PF_MD, ETAT_OK_NON, FUITES_CHOICES, DECISION_CHOICES, PARTIE_CHOICES


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


#  documents legaux forms.py
from django import forms
from .models import AssuranceEngin, Engin

class AssuranceEnginForm(forms.ModelForm):
    engin = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Engin"
    )

    type_assurance = forms.ChoiceField(
        choices=AssuranceEngin.ASSURANCE_TYPES,
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Type Assurance"
    )

    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date Début"
    )

    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date Validité"
    )

    observations = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label="Observations"
    )

    nom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Assureur"
    )

    class Meta:
        model = AssuranceEngin
        fields = ['engin', 'nom', 'type_assurance', 'date_debut', 'date_fin', 'observations']

# forms.py
from django import forms
from .models import VignetteConformite, Engin

class VignetteConformiteForm(forms.ModelForm):
    engin = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Engin"
    )
    type_vignette = forms.ChoiceField(
        choices=VignetteConformite.TYPES_VIGNETTE,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Type de vignette"
    )
    date_emission = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date d'émission"
    )
    date_expire = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date d'expiration"
    )
    observations = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label="Observations"
    )

    class Meta:
        model = VignetteConformite
        fields = ['engin', 'type_vignette', 'date_emission', 'date_expire', 'observations']


from django import forms
from .models import ControleTechnique, Engin
from documents.forms import FichierJointForm
from documents.models import DocumentType

class ControleTechniqueForm(forms.ModelForm):
    class Meta:
        model = ControleTechnique
        fields = [
            'engin', 
            'date_controle', 
            'resultat', 
            'commentaire', 
            'centre_controle', 
            'inspecteur', 
            'validite_mois', 
            'actions_correctives'
        ]

        widgets = {
            'engin': forms.Select(attrs={'class': 'form-select'}),
            'date_controle': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'resultat': forms.Select(attrs={'class': 'form-select'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'centre_controle': forms.TextInput(attrs={'class': 'form-control'}),
            'inspecteur': forms.TextInput(attrs={'class': 'form-control'}),
            'validite_mois': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'actions_correctives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'engin': "Engin",
            'date_controle': "Date du contrôle",
            'resultat': "Résultat",
            'commentaire': "Commentaire",
            'centre_controle': "Centre de contrôle",
            'inspecteur': "Inspecteur",
            'validite_mois': "Validité (mois)",
            'actions_correctives': "Actions correctives",
        }

# ⚡ Formulaire pour les documents liés au contrôle
class ControleTechniqueDocumentForm(FichierJointForm):
    def __init__(self, *args, **kwargs):
        # On force le module "ControleTechnique" pour filtrer les types de documents
        kwargs['module'] = 'ControleTechnique'
        super().__init__(*args, **kwargs)
        self.fields['fichier'].required = False  # Le fichier peut être optionnel


class CertificatJaugeageForm(forms.ModelForm):
    engin = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Engin"
    )

    numero_certificat = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Numéro du certificat"
    )

    date_jaugeage = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date de jaugeage"
    )

    validite_mois = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        label="Validité (mois)"
    )

    organisme = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Organisme"
    )

    observations = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Observations"
    )

    class Meta:
        model = CertificatJaugeage
        fields = ['engin', 'numero_certificat', 'date_jaugeage', 'validite_mois', 'organisme', 'observations']

# ⚡ Optionnel : Formulaire pour documents joints liés au certificat
class CertificatJaugeageDocumentForm(FichierJointForm):
    def __init__(self, *args, **kwargs):
        kwargs['module'] = 'CertificatJaugeage'
        super().__init__(*args, **kwargs)
        self.fields['fichier'].required = False


from django import forms
from django.core.exceptions import ValidationError
from engins.models import EvenementEngin

class EvenementEnginForm(forms.ModelForm):

    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Date de début"
    )

    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Date de fin"
    )

    definitif = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Événement définitif (sans date de fin)"
    )

    class Meta:
        model = EvenementEngin
        fields = [
            "engin",
            "type_evenement",
            "flotte_initiale",
            "flotte_beneficiaire",
            "description",
            "statut_camion",
            "statut_radar",
            "date_debut",
            "date_fin",
            "definitif",
            "valideur",
            "observations",
        ]

        widgets = {
            "engin": forms.Select(attrs={"class": "form-control"}),
            "type_evenement": forms.Select(attrs={"class": "form-control"}),
            "statut_camion": forms.Select(attrs={"class": "form-control"}),
            "statut_radar": forms.Select(attrs={"class": "form-control"}),
            "valideur": forms.Select(attrs={"class": "form-control"}),

            "flotte_initiale": forms.Select(attrs={"class": "form-control"}),
            "flotte_beneficiaire": forms.Select(attrs={"class": "form-control"}),


            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
            "observations": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")
        definitif = cleaned_data.get("definitif")

        if date_fin and date_debut and date_fin < date_debut:
            raise ValidationError(
                "La date de fin ne peut pas être antérieure à la date de début."
            )

        if definitif:
            cleaned_data["date_fin"] = None

        return cleaned_data
