from django import forms
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from .models import Societe, Ville, Site, Departement, Service, Fonction

# =========================
# Formulaire Société
# =========================
class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = ['libelle', 'date_integration', 'actif']
        widgets = {
            'date_integration': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajoute la classe 'form-control' à tous les champs sauf 'actif'
        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    # Validation pour éviter les doublons insensibles à la casse
    def clean_libelle(self):
        libelle = self.cleaned_data['libelle'].strip()
        qs = Societe.objects.filter(libelle__iexact=libelle)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Une société avec ce nom existe déjà.")
        return libelle


# =========================
# Formulaire Ville
# =========================
class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = ['pays', 'libelle', 'actif']
        widgets = {
            'pays': CountrySelectWidget(attrs={'class': 'form-control'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    # Validation : pas de doublon pour le même pays
    def clean_libelle(self):
        libelle = self.cleaned_data.get('libelle')
        pays = self.cleaned_data.get('pays')
        qs = Ville.objects.filter(libelle__iexact=libelle, pays=pays)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Cette ville existe déjà pour ce pays.")
        return libelle


# =========================
# Formulaire Site
# =========================
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['nom_site', 'adresse', 'description', 'actif']
        widgets = {
            'nom_site': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    # Validation nom unique
    def clean_nom_site(self):
        nom_site = self.cleaned_data.get('nom_site')
        qs = Site.objects.filter(nom_site__iexact=nom_site)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Un site avec ce nom existe déjà.")
        return nom_site

    # Validation adresse
    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')
        if adresse and len(adresse) < 5:
            raise ValidationError("L'adresse est trop courte.")
        return adresse


# =========================
# Formulaire Département
# =========================
class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    # Validation nom unique
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        qs = Departement.objects.filter(nom__iexact=nom)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Un département avec ce nom existe déjà.")
        return nom


# =========================
# Formulaire Service
# =========================
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'departement', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ne montrer que les départements actifs
        self.fields['departement'].queryset = Departement.objects.filter(actif=True)

    # Validation : pas de doublon dans le même département
    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom')
        departement = cleaned_data.get('departement')
        if nom and departement:
            qs = Service.objects.filter(nom__iexact=nom, departement=departement)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Un service avec ce nom existe déjà dans ce département.")
        return cleaned_data


# =========================
# Formulaire Fonction
# =========================
class FonctionForm(forms.ModelForm):
    class Meta:
        model = Fonction
        fields = ['nom', 'service', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    # Validation : pas de doublon pour le même service
    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom')
        service = cleaned_data.get('service')
        if nom and service:
            qs = Fonction.objects.filter(nom__iexact=nom, service=service)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Une fonction avec ce nom existe déjà dans ce service.")
        return cleaned_data
