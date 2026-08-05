# engins/models/evenements.py

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from engins.models import Engin
from personnel.models import Employe
from documents.models import FichierJoint
from engins.models import TimeStampedModel, SlugModel, StatusModel


# =========================
# STATUT RADAR
# =========================
class StatutRadarEvenement(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Statut Radar"
        verbose_name_plural = "Statuts Radar"
        ordering = ["nom"]

# =========================
# TYPE EVENEMENT
# =========================
class TypeEvenement(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, TypeEvenement.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

# =========================
# STATUT CAMION EVENEMENT
# =========================
class StatutCamionEvenement(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, StatutCamionEvenement.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

# =========================
# EVENEMENT ENGIN
# =========================
class EvenementEngin(TimeStampedModel, StatusModel, SlugModel):
    code_evenement = models.CharField(max_length=20, unique=True, editable=False)
    
    engin = models.ForeignKey(
        Engin,
        on_delete=models.PROTECT,
        related_name="evenements"
    )

    type_evenement = models.ForeignKey(
        TypeEvenement,
        on_delete=models.PROTECT
    )

    flotte_initiale = models.ForeignKey(
    'flotte.Flotte',  # chaîne = lazy reference
    on_delete=models.PROTECT,
    related_name="evenements_initiaux"
    )
    flotte_beneficiaire = models.ForeignKey(
        'flotte.Flotte',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="evenements_beneficiaires"
    )

    description = models.TextField()

    statut_camion = models.ForeignKey(
        StatutCamionEvenement,
        on_delete=models.PROTECT
    )

    statut_radar = models.ForeignKey(
        StatutRadarEvenement,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    duree_jours = models.PositiveIntegerField(blank=True, null=True, editable=False)
    definitif = models.BooleanField(default=False)

    responsable_saisie = models.ForeignKey(
        Employe,
        on_delete=models.PROTECT,
        related_name="evenements_saisis"
    )

    valideur = models.ForeignKey(
        Employe,
        on_delete=models.PROTECT,
        related_name="evenements_valides"
    )

    observations = models.TextField(blank=True, null=True)

    pieces_jointes = GenericRelation(
        FichierJoint,
        related_query_name="evenements"
    )

    # ======================
    # LOGIQUE METIER
    # ======================
    def clean(self):
        if self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError("La date de fin ne peut pas être antérieure à la date de début.")

    def save(self, *args, **kwargs):
        # Génération du code EVT-0001
        if not self.code_evenement:
            last = EvenementEngin.objects.order_by("id").last()
            next_id = last.id + 1 if last else 1
            self.code_evenement = f"EVT-{next_id:04d}"

        # Slug sécurisé
        if not self.slug:
            self.slug = self.generate_unique_slug(self.code_evenement, EvenementEngin.objects)

        # Calcul durée
        if self.date_debut and self.date_fin and not self.definitif:
            self.duree_jours = (self.date_fin - self.date_debut).days
        else:
            self.duree_jours = None
            if self.definitif:
                self.date_fin = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_evenement

    class Meta:
        verbose_name = "Événement Engin"
        verbose_name_plural = "Événements Engins"
        ordering = ["-date_debut"]
