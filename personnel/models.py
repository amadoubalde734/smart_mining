# ===============================
# personnel/models.py
# ===============================

from django.db import models
from django.utils.text import slugify
from parametrage.models import Ville, Site, Departement, Service, Societe
from django.contrib.auth import get_user_model
User = get_user_model()


# ===============================
# MIXINS
# ===============================
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    actif = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(max_length=191, unique=True, blank=True)

    def generate_unique_slug(self, field_value, queryset):
        base_slug = slugify(field_value)
        slug = base_slug
        counter = 1
        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    class Meta:
        abstract = True


# ===============================
# EMPLOYE
# ===============================
class Employe(TimeStampedModel, StatusModel, SlugModel):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=150, blank=True, null=True)
    sexe_choices = [('M', 'Masculin'), ('F', 'Féminin')]
    sexe = models.CharField(max_length=1, choices=sexe_choices, blank=True, null=True)
    fonction = models.CharField(max_length=100, blank=True, null=True)

    # Liens vers parametrage
    societe = models.ForeignKey(Societe, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    ville = models.ForeignKey(Ville, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')

    # Responsable hiérarchique
    responsable = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordonnes',
        verbose_name="Responsable hiérarchique"
    )

    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    date_embauche = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='employes/photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Génération du slug unique
        if not self.slug:
            self.slug = self.generate_unique_slug(f"{self.nom}-{self.prenoms}-{self.matricule}", Employe.objects)
        super().save(*args, **kwargs)

    def clean(self):
        # Validation : le responsable est obligatoire sauf si c'est le premier employé
        if not self.responsable and Employe.objects.exists():
            from django.core.exceptions import ValidationError
            raise ValidationError("Un responsable hiérarchique doit être renseigné pour cet employé.")

    def __str__(self):
        return f"{self.nom} {self.prenoms} ({self.matricule})"


# ===============================
# HISTORIQUE EMPLOYE
# ===============================
class HistoriqueEmploye(TimeStampedModel, StatusModel):
    # Liste d'actions standardisées
    ACTION_CHOICES = [
        ('CREATION', 'Création'),
        ('MODIFICATION', 'Modification'),
        ('PROMOTION', 'Promotion'),
        ('DEPART', 'Départ'),
        ('CONGES', 'Congés'),
        ('FORMATION', 'Formation'),
        ('HABILITATION', 'Habilitation'),
        ('CHANGEMENT_RESPONSABLE', 'Changement de responsable')
    ]

    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name='historiques',
        verbose_name="Employé"
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        verbose_name="Type d'action"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description / Détails"
    )
    date_action = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'action")
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Utilisateur ayant effectué l'action"
    )

    class Meta:
        verbose_name = "Historique Employé"
        verbose_name_plural = "Historiques Employés"
        ordering = ['-date_action']
        indexes = [
            models.Index(fields=['employe', 'date_action']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} - {self.employe.nom} {self.employe.prenoms} le {self.date_action.strftime('%d/%m/%Y %H:%M')}"
