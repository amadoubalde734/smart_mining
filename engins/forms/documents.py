# Django
from django import forms
from django.core.exceptions import ValidationError

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
    CategorieEngin
)
from engins.models.documents_legaux import CarteGrise
from documents.models import FichierJoint, DocumentType

# =========================
# FORMS
# =========================
from documents.forms import FichierJointForm
# Formulaire pour l'Assurance d'un Engin
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


# Formulaire pour la Vignette de Conformité d'un Engin
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


# Formulaire pour le Contrôle Technique d'un Engin
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


# Formulaire pour les documents liés au contrôle technique
class ControleTechniqueDocumentForm(FichierJointForm):
    def __init__(self, *args, **kwargs):
        kwargs['module'] = 'ControleTechnique'  # Filtrage des types de documents
        super().__init__(*args, **kwargs)
        self.fields['fichier'].required = False  # Le fichier peut être optionnel


# Formulaire pour le Certificat de Jaugeage d'un Engin
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


# Formulaire pour les documents joints liés au certificat de jaugeage
class CertificatJaugeageDocumentForm(FichierJointForm):
    def __init__(self, *args, **kwargs):
        kwargs['module'] = 'CertificatJaugeage'  # Filtrage des types de documents
        super().__init__(*args, **kwargs)
        self.fields['fichier'].required = False  # Le fichier peut être optionnel


class CarteGriseForm(forms.ModelForm):
    engin = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        required=False,
        label="Engin principal"
    )
    remorque = forms.ModelChoiceField(
        queryset=Remorque.objects.all(),
        required=False,
        label="Remorque (si applicable)"
    )
    citerne = forms.ModelChoiceField(
        queryset=Citerne.objects.all(),
        required=False,
        label="Citerne (si applicable)"
    )
    fichier = forms.FileField(
        required=True,  # obligatoire comme dans ton template
        label="Document Carte Grise"
    )

    class Meta:
        model = CarteGrise
        fields = [
            "numero",
            "date_delivrance",
            "date_expiration",
            "observations",
            "engin",
            "remorque",
            "citerne",
        ]

    def clean(self):
        cleaned_data = super().clean()
        engin = cleaned_data.get("engin")
        remorque = cleaned_data.get("remorque")
        citerne = cleaned_data.get("citerne")

        if not engin and not remorque and not citerne:
            raise ValidationError("Vous devez sélectionner au moins un engin, une remorque ou une citerne.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Sauvegarder le fichier joint
            fichier = self.cleaned_data.get("fichier")
            if fichier:
                FichierJoint.objects.create(
                    titre="Carte Grise",
                    fichier=fichier,
                    content_object=instance
                )
        return instance