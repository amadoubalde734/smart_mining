from django import forms
from .models import BonCommande, BonCommandeLigne, BonLivraison, BonLivraisonLigne

class BonCommandeForm(forms.ModelForm):
    class Meta:
        model = BonCommande
        fields = ['numero', 'client', 'date_commande', 'description', 'code_budgetaire',
                  'compte_analytique', 'tva', 'remise', 'statut']

        widgets = {
            'date_commande': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'remise': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BonCommandeLigneForm(forms.ModelForm):
    class Meta:
        model = BonCommandeLigne
        fields = ['produit', 'description', 'quantite', 'unite', 'prix_unitaire']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BonLivraisonForm(forms.ModelForm):
    class Meta:
        model = BonLivraison
        fields = ['numero', 'bon_commande', 'date_livraison', 'site', 'transporteur', 'observations', 'statut']

        widgets = {
            'date_livraison': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

class BonLivraisonLigneForm(forms.ModelForm):
    class Meta:
        model = BonLivraisonLigne
        fields = ['produit', 'description', 'quantite', 'unite']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
        }
