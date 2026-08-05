# documents/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import FichierJoint, DocumentType

class FichierJointForm(forms.ModelForm):
    type_document = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Type de document"
    )

    def __init__(self, *args, **kwargs):
        # On peut passer 'module' pour filtrer les types de documents
        module = kwargs.pop('module', None)
        super().__init__(*args, **kwargs)
        if module:
            self.fields['type_document'].queryset = DocumentType.objects.filter(modele=module)

    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if fichier:
            # Taille max 5 Mo
            if fichier.size > 5 * 1024 * 1024:
                raise ValidationError("Le fichier ne doit pas dépasser 5 Mo.")
            # Extensions autorisées
            ext = fichier.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png', 'docx', 'xlsx']:
                raise ValidationError("Format de fichier non autorisé (pdf, jpg, jpeg, png, docx, xlsx).")
        return fichier

    class Meta:
        model = FichierJoint
        fields = ['titre', 'fichier', 'description', 'type_document']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'fichier': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
