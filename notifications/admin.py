from django.contrib import admin
from django import forms
from .models import ParametrageRapport

# Choix disponibles
STATUTS_CHOICES = [
    ("non_demarree", "Non démarrée"),
    ("en_cours", "En cours"),
    ("prévue", "Prévue"),
    ("terminee", "Terminée"),
]

ROLES_CHOICES = [
    ("ROLE_QSE_TEAM", "QSE Team"),
    ("ROLE_ADMIN", "Admin"),
    ("ROLE_TOP_MANAGEMENT", "Top Management"),
    ("ROLE_RESPONSABLE_PROCESSUS", "Responsable Processus"),
]

class ParametrageRapportForm(forms.ModelForm):
    statuts = forms.MultipleChoiceField(
        choices=STATUTS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Sélectionnez les statuts des actions à inclure.'
    )

    roles_en_copie = forms.MultipleChoiceField(
        choices=ROLES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Sélectionnez les rôles des utilisateurs à mettre en copie.'
    )
    
    class Meta:
        model = ParametrageRapport
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser les champs avec les listes stockées dans la base
        if self.instance and self.instance.pk:
            self.fields['statuts'].initial = self.instance.statuts
            self.fields['roles_en_copie'].initial = self.instance.roles_en_copie

    def clean_statuts(self):
        return self.cleaned_data.get('statuts', [])

    def clean_roles_en_copie(self):
        return self.cleaned_data.get('roles_en_copie', [])

@admin.register(ParametrageRapport)
class ParametrageRapportAdmin(admin.ModelAdmin):
    form = ParametrageRapportForm
    list_display = ('jours_avant',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(request, "🔄 Paramétrage mis à jour avec succès.")
        else:
            self.message_user(request, "✅ Nouveau paramétrage enregistré avec succès.")
