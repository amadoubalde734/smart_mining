from django import forms

from engins.models import (
    TypeEngin,
    CategorieEngin,
    Marque,
    Modele,
    StatutEngin,
    SiteEngin,
    Engin,
    Remorque,
    Citerne,
)

from personnel.models import Employe

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
            'date_mise_circulation', 'date_integration',
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
            'date_integration': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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


