
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
