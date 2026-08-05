from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Societe
from backend.models import Ville, Site # Importation correcte des modèles

# Formulaire Societe
class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = ['libelle', 'date_integration', 'statut']
        widgets = {
            'date_integration': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'statut': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # Ne pas forcer form-control sur le checkbox
            if name != 'statut':
                field.widget.attrs.update({'class': 'form-control'})

# Formulaire Ville
class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = ['pays', 'libelle', 'statut']
        widgets = {
            'pays': CountrySelectWidget(attrs={'class': 'form-control'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'statut':
                field.widget.attrs.update({'class': 'form-control'})

# Formulaire Site
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['nom_site', 'adresse', 'description', 'statut']
        widgets = {
            'nom_site': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'statut': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'statut':
                field.widget.attrs.update({'class': 'form-control'})
