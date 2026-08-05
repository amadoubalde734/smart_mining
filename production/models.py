from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

# Models externes
from engins.models import Engin, SiteEngin
from personnel.models import Employe
from documents.models import FichierJoint
from commercial.models import BonLivraison

# ===============================
# PARAMÉTRAGE PRODUCTION
# ===============================
class Pit(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class UniteProduction(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

class Shift(models.Model):
    nom = models.CharField(max_length=50)  # Jour / Nuit / A / B / C

    def __str__(self):
        return self.nom

class Transporteur(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class LieuDechargement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# ===============================
# PRODUCTION ENGINS
# ===============================
class ProductionEngin(models.Model):
    engin = models.ForeignKey(Engin, on_delete=models.CASCADE, related_name="productions")
    chauffeur = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name="productions")
    date_heure_chargement = models.DateTimeField()
    date_heure_dechargement = models.DateTimeField(null=True, blank=True)
    pit = models.ForeignKey(Pit, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(SiteEngin, on_delete=models.SET_NULL, null=True, blank=True, related_name="productions")
    unite = models.ForeignKey(UniteProduction, on_delete=models.SET_NULL, null=True)
    type_cam = models.CharField(max_length=50)
    bon_livraison = models.ForeignKey(
        BonLivraison,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productions"
    )
    volume_m3 = models.DecimalField("Volume (m³)", max_digits=10, decimal_places=2)
    poids_brut = models.DecimalField("Poids brut (T)", max_digits=10, decimal_places=2)
    poids_vide = models.DecimalField("Poids à vide (T)", max_digits=10, decimal_places=2)
    poids_net = models.DecimalField("Poids net (T)", max_digits=10, decimal_places=2)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)
    transporteur = models.ForeignKey(Transporteur, on_delete=models.SET_NULL, null=True)
    objectif_mt_jour = models.DecimalField("Objectif MT / jour", max_digits=10, decimal_places=2, null=True, blank=True)
    observations = models.TextField(blank=True, null=True)
    fichiers = GenericRelation(FichierJoint, related_query_name="productions")
    slug = models.SlugField(max_length=191, unique=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productions_crees"
    )

    class Meta:
        ordering = ["-date_heure_chargement"]
        verbose_name = "Production Engin"
        verbose_name_plural = "Productions Engins"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Attention : self.numero_bl doit exister dans ton modèle ou être remplacé par un champ existant
            self.slug = slugify(f"{self.engin.immatriculation}-{self.bon_livraison.id if self.bon_livraison else 'BL'}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.engin} | BL {self.bon_livraison.id if self.bon_livraison else 'N/A'}"