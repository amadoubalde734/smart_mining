# personnel/forms.py
from django import forms
from .models import Employe
from parametrage.models import Societe, Departement, Service, Site, Ville, Fonction

# =========================
# FORMULAIRE EMPLOYÉ
# =========================
class EmployeForm(forms.ModelForm):
    # -------------------------
    # Champ Fonction dynamique
    # -------------------------
    fonction = forms.ModelChoiceField(
        queryset=Fonction.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_fonction'})
    )

    # -------------------------
    # Champ Responsable
    # -------------------------
    responsable = forms.ModelChoiceField(
        queryset=Employe.objects.none(),  # sera rempli dans __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Responsable hiérarchique"
    )

    class Meta:
        model = Employe
        fields = [
            'matricule', 'nom', 'prenoms', 'date_naissance', 'lieu_naissance', 'sexe',
            'fonction', 'responsable', 'societe', 'departement', 'service', 'site', 'ville',
            'email', 'telephone', 'adresse', 'date_embauche', 'photo', 'actif'
        ]
        widgets = {
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'societe': forms.Select(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-control', 'id': 'id_departement'}),
            'service': forms.Select(attrs={'class': 'form-control', 'id': 'id_service'}),
            'site': forms.Select(attrs={'class': 'form-control'}),
            'ville': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Appliquer 'form-control' à tous les champs sauf photo, actif, fonction, responsable
        for name, field in self.fields.items():
            if name not in ['photo', 'actif', 'fonction', 'responsable']:
                field.widget.attrs.update({'class': 'form-control'})

        # =============================
        # Définir queryset du champ fonction
        # =============================
        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['fonction'].queryset = Fonction.objects.filter(
                    service_id=service_id,
                    actif=True
                ).order_by('nom')
            except (ValueError, TypeError):
                self.fields['fonction'].queryset = Fonction.objects.none()
        elif self.instance.pk and self.instance.service:
            self.fields['fonction'].queryset = Fonction.objects.filter(
                service=self.instance.service,
                actif=True
            ).order_by('nom')
        else:
            self.fields['fonction'].queryset = Fonction.objects.none()

        # =============================
        # Définir queryset du champ responsable
        # =============================
        # Exclure l'employé lui-même pour éviter qu'il se soit son propre responsable
        if self.instance.pk:
            self.fields['responsable'].queryset = Employe.objects.exclude(pk=self.instance.pk).order_by('nom')
        else:
            self.fields['responsable'].queryset = Employe.objects.all().order_by('nom')

    # =========================
    # Validation du matricule unique
    # =========================
    def clean_matricule(self):
        matricule = self.cleaned_data.get('matricule')
        qs = Employe.objects.filter(matricule__iexact=matricule)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ce matricule est déjà utilisé pour un autre employé.")
        return matricule

    # =========================
    # Validation email unique
    # =========================
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = Employe.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Cet email est déjà utilisé pour un autre employé.")
        return email
