from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput

# Après
from .models import (
    FormationChauffeur,
    SuiviPASSMine,
    PermisTravail,
    ComportementConduite,
    Site
)
from personnel.models import Employe
from django import forms
from django.core.exceptions import ValidationError
from personnel.models import Employe
from parametrage.models import Site
from .models import SuiviPASSMine
from parametrage.models import Site, Service
from flotte.models import Flotte
from engins.models import CategorieEngin



# ===============================
# Widget personnalisé pour upload multiple
# ===============================
class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


# ===============================
# Mixin Bootstrap (UNE SEULE FOIS)
# ===============================
class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')

            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.setdefault('class', 'form-control')

            else:
                field.widget.attrs.setdefault('class', 'form-control')
               # ===============================
# Formulaire pour Formation Chauffeur ERP-ready
# ===============================

class FormationChauffeurForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = FormationChauffeur
        fields = [
            # --- Références ---
            'employe',
            'formateur',
            'type_formation',
            'site',
            'flotte',
            'service',
            'categorie_engin',

            # --- Détails formation ---
            'motif_theme',
            'date_formation',
            'heure_debut',
            'heure_fin',
            'duree_jours',
            'organisme',

            # --- Qualification & évaluation ---
            'qualification_actuelle',
            'note',
            'appreciation',
            'score',
            'nombre_formation',

            # --- Divers ---
            'validite',
            'jours_avant_expiration',
            'statut',
            'observation',
        ]

        widgets = {
            'date_formation': forms.DateInput(attrs={'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'validite': forms.DateInput(attrs={'type': 'date'}),

            'motif_theme': forms.TextInput(attrs={'placeholder': 'Ex : Recyclage conduite défensive'}),
            'score': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Ex : 42.50'}),
            'jours_avant_expiration': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Ex : 30'}),
            'observation': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

        # --- Querysets filtrés ---
        self.fields['employe'].queryset = Employe.objects.filter(actif=True)
        self.fields['formateur'].queryset = Employe.objects.filter(actif=True)
        self.fields['site'].queryset = Site.objects.filter(actif=True)
        self.fields['service'].queryset = Service.objects.filter(actif=True)
        self.fields['flotte'].queryset = Flotte.objects.filter(actif=True)
        self.fields['categorie_engin'].queryset = CategorieEngin.objects.filter(actif=True)

        # --- Correction pour Qualification actuelle ---
        self.fields['qualification_actuelle'].widget = forms.Select(choices=FormationChauffeur.QUALIFICATION_CHOICES)

    # ===============================
    # VALIDATIONS MÉTIER
    # ===============================

    def clean_validite(self):
        date_formation = self.cleaned_data.get('date_formation')
        validite = self.cleaned_data.get('validite')

        if validite and date_formation and validite < date_formation:
            raise ValidationError(
                "La date de validité ne peut pas être antérieure à la date de formation."
            )
        return validite

    def clean(self):
        cleaned_data = super().clean()

        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')
        duree_jours = cleaned_data.get('duree_jours')
        formateur = cleaned_data.get('formateur')
        employe = cleaned_data.get('employe')

        if heure_debut and heure_fin and heure_fin <= heure_debut:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")

        if duree_jours is not None and duree_jours <= 0:
            raise ValidationError("La durée de la formation doit être supérieure à 0 jour.")

        if formateur and employe and formateur == employe:
            raise ValidationError("Le formateur ne peut pas être le même que l'employé.")

        return cleaned_data
    
# ===============================
# Formulaire ERP-ready pour Suivi PASS Mine
# ===============================
class SuiviPASSMineForm(BootstrapFormMixin, forms.ModelForm):
    fichiers_joints = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True}),
        label="Fichiers joints"
    )

    class Meta:
        model = SuiviPASSMine
        fields = [
            'employe',
            'numero_pass',
            'type_pass',
            'date_emission',
            'date_expiration',
            'responsable',
            'site_emission',
            'jours_avant_expiration',
            'statut',
            'observation'
        ]
        widgets = {
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
            'date_expiration': forms.DateInput(attrs={'type': 'date'}),
            'observation': forms.Textarea(attrs={'rows': 3}),
            'jours_avant_expiration': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer le style bootstrap
        self.apply_bootstrap()
        # Filtrer les queryset pour ERP-friendly
        self.fields['employe'].queryset = Employe.objects.filter(actif=True)
        self.fields['responsable'].queryset = Employe.objects.filter(actif=True)
        self.fields['site_emission'].queryset = Site.objects.filter(actif=True)

    def clean_date_expiration(self):
        date_emission = self.cleaned_data.get('date_emission')
        date_expiration = self.cleaned_data.get('date_expiration')
        if date_expiration and date_emission and date_expiration < date_emission:
            raise ValidationError(
                "La date d'expiration doit être postérieure à la date d'émission."
            )
        return date_expiration

# ==============================
# Formulaire pour Permis de Travail        
# ==============================

class PermisTravailForm(BootstrapFormMixin, forms.ModelForm):
    
    fichiers_joints = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True}),
        label="Fichiers joints"
    )

    class Meta:
        model = PermisTravail
        fields = [
            'employe',
            'type_permis',
            'date_emission',
            'date_expiration',
            'responsable',
            'site_emission',
            'observation'
        ]
        widgets = {
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
            'date_expiration': forms.DateInput(attrs={'type': 'date'}),
            'observation': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        # Limiter les employés actifs
        self.fields['employe'].queryset = Employe.objects.filter(actif=True)
        self.fields['responsable'].queryset = Employe.objects.filter(actif=True)

    def clean_date_expiration(self):
        date_emission = self.cleaned_data.get('date_emission')
        date_expiration = self.cleaned_data.get('date_expiration')
        if date_expiration and date_emission and date_expiration < date_emission:
            raise ValidationError(
                "La date d'expiration doit être postérieure à la date d'émission."
            )
        return date_expiration
    
    
# ==============================
# Formulaire pour Comportement et Conduite  
class ComportementConduiteForm(BootstrapFormMixin, forms.ModelForm):

    fichiers_joints = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True}),
        label="Fichiers joints"
    )

    class Meta:
        model = ComportementConduite
        fields = [
            'employe',
            'responsable',         # Ajout du responsable
            'evaluateur',
            'date_evaluation',
            'type_evaluation',
            'evaluation',
            'score',
            'niveau',
            'statut',
            'observation',
            'action_corrective'
        ]
        widgets = {
            'date_evaluation': forms.DateInput(attrs={'type': 'date'}),
            'evaluation': forms.Textarea(attrs={'rows': 3}),
            'observation': forms.Textarea(attrs={'rows': 3}),
            'action_corrective': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

        # Querysets pour les ForeignKey
        self.fields['employe'].queryset = Employe.objects.filter(actif=True)
        self.fields['responsable'].queryset = Employe.objects.filter(actif=True)
        self.fields['evaluateur'].queryset = Employe.objects.filter(actif=True)

        # Champs à sélection vide par défaut
        self.fields['type_evaluation'].empty_label = "Sélectionnez un type"
        self.fields['niveau'].empty_label = "Sélectionnez un niveau"
        self.fields['statut'].empty_label = "Sélectionnez un statut"

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and not (0 <= score <= 100):
            raise ValidationError("Le score doit être compris entre 0 et 100.")
        return score
