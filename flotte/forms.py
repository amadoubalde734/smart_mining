from django import forms
from .models import Flotte

class FlotteForm(forms.ModelForm):
    class Meta:
        model = Flotte
        fields = ["nom", "description", "site", "engins", "actif"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "site": forms.Select(attrs={"class": "form-control"}),
            "engins": forms.SelectMultiple(attrs={"class": "form-control"}),
            "actif": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


