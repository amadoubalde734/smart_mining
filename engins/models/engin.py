from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from personnel.models import Employe
from parametrage.models import Societe
from documents.models import FichierJoint

# ===============================
# MIXINS PRO
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
# TYPES D'ENGINS
# ===============================
class TypeEngin(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, TypeEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Type d'engin"
        verbose_name_plural = "Types d'engins"

# ===============================
# CATEGORIES D'ENGINS
# ===============================
class CategorieEngin(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, CategorieEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Catégorie d'engin"
        verbose_name_plural = "Catégories d'engins"

# ===============================
# MARQUES ET MODELES
# ===============================
class Marque(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Marque"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, Marque.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Marque"
        verbose_name_plural = "Marques"

class Modele(TimeStampedModel, StatusModel, SlugModel):
    marque = models.ForeignKey(
        Marque,
        on_delete=models.CASCADE,
        related_name="modeles"
    )

    type_engin = models.ForeignKey(
        TypeEngin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nom = models.CharField(
        max_length=100,
        verbose_name="Modèle"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.marque.nom}-{self.nom}"
            self.slug = self.generate_unique_slug(base, Modele.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marque.nom} {self.nom}"

    class Meta:
        ordering = ["marque__nom", "nom"]
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        unique_together = ("marque", "nom", "type_engin")


# ===============================
# STATUTS DES ENGINS
# ===============================
class StatutEngin(TimeStampedModel, StatusModel, SlugModel):
    STATUTS = [
        ("DISPONIBLE", "Disponible"),
        ("MAINTENANCE", "Maintenance"),
        ("EN_SERVICE", "En service"),
        ("HORS_SERVICE", "Hors service"),
    ]

    nom = models.CharField(max_length=50, choices=STATUTS)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, StatutEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Statut d'engin"
        verbose_name_plural = "Statuts d'engins"

# ===============================
# SITES / DEPOTS
# ===============================
class SiteEngin(TimeStampedModel, StatusModel, SlugModel):
    nom_site = models.CharField(max_length=150)
    adresse = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom_site, SiteEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_site

    class Meta:
        ordering = ["nom_site"]
        verbose_name = "Site / Dépôt"
        verbose_name_plural = "Sites / Dépôts"

# ===============================
# ENGINS
# ===============================
class Engin(TimeStampedModel, StatusModel, SlugModel):
    immatriculation = models.CharField(max_length=50, unique=True)
    numero_chassis = models.CharField(max_length=50, blank=True, null=True)
    marque = models.ForeignKey(
        Marque,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="engins"
    )

    modele = models.ForeignKey(
        Modele,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="engins"
    )
    couleur = models.CharField(max_length=50, blank=True, null=True)
    date_mise_circulation = models.DateField(blank=True, null=True)
    date_integration = models.DateField(blank=True, null=True)
    proprietaire = models.ForeignKey(Societe, on_delete=models.SET_NULL, null=True, blank=True)
    contact_proprietaire = models.CharField(max_length=50, blank=True, null=True)
    type_chassis = models.CharField(max_length=50, blank=True, null=True)
    nombre_essieux = models.PositiveIntegerField(blank=True, null=True)
    volume_benne_citerne = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_fermeture_benne = models.CharField(max_length=50, blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    site = models.ForeignKey(SiteEngin, on_delete=models.SET_NULL, null=True, blank=True)
    type_engin = models.ForeignKey(TypeEngin, on_delete=models.SET_NULL, null=True, blank=True)
    categorie = models.ForeignKey(CategorieEngin, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.ForeignKey(StatutEngin, on_delete=models.SET_NULL, null=True, blank=True)
    camion_communautaire = models.BooleanField(default=False)
    fichiers = GenericRelation(FichierJoint, related_query_name='engins')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.immatriculation, Engin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.immatriculation

    class Meta:
        ordering = ["immatriculation"]
        verbose_name = "Engin"
        verbose_name_plural = "Engins"

    def clean(self):
        super().clean()
        titres_fichiers = [f.titre.lower() for f in self.fichiers.all()]
        obligatoires = ["carte grise", "assurance", "photo engin"]
        for titre in obligatoires:
            if titre not in titres_fichiers:
                raise ValidationError(f"Le fichier obligatoire '{titre}' est manquant pour cet engin.")

        if self.type_engin:
            nom_type = self.type_engin.nom.lower()
            if "citerne" in nom_type and not self.citernes.exists():
                raise ValidationError("Un camion citerne doit avoir au moins une citerne.")
            if "benne" in nom_type and not self.remorques.exists():
                raise ValidationError("Un camion benne doit avoir au moins une remorque (benne).")

# ===============================
# REMORQUES
# ===============================
class Remorque(TimeStampedModel, StatusModel, SlugModel):
    TYPE_REMORQUE_CHOICES = [
        ("benne", "Benne"),
        ("autre", "Autre"),
    ]

    immatriculation = models.CharField(max_length=50, unique=True)
    numero_chassis = models.CharField(max_length=50, blank=True, null=True)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50, blank=True, null=True)
    volume_benne_citerne = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_remorque = models.CharField(max_length=20, choices=TYPE_REMORQUE_CHOICES, default="benne")

    tracteur = models.ForeignKey(Engin, on_delete=models.CASCADE, related_name="remorques")
    fichiers = GenericRelation(FichierJoint, related_query_name='remorques')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(f"{self.tracteur.immatriculation}-{self.immatriculation}", Remorque.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Remorque {self.immatriculation} ({self.type_remorque}) du tracteur {self.tracteur.immatriculation}"

    class Meta:
        ordering = ["immatriculation"]
        verbose_name = "Remorque"
        verbose_name_plural = "Remorques"

    def clean(self):
        super().clean()
        titres_fichiers = [f.titre.lower() for f in self.fichiers.all()]
        obligatoires = ["carte grise", "assurance", "photo engin"]
        for titre in obligatoires:
            if titre not in titres_fichiers:
                raise ValidationError(f"Le fichier obligatoire '{titre}' est manquant pour cette remorque.")
        if self.type_remorque == "benne" and not self.volume_benne_citerne:
            raise ValidationError("Le volume de la benne doit être renseigné pour une remorque de type benne.")

# ===============================
# CITERNE
# ===============================
class Citerne(TimeStampedModel, StatusModel, SlugModel):
    numero_serie = models.CharField(max_length=50, unique=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_fermeture = models.CharField(max_length=50, blank=True, null=True)
    engin = models.ForeignKey(Engin, on_delete=models.CASCADE, null=True, blank=True, related_name="citernes")
    remorque = models.ForeignKey(Remorque, on_delete=models.CASCADE, null=True, blank=True, related_name="citernes")
    fichiers = GenericRelation(FichierJoint, related_query_name='citernes')

    def save(self, *args, **kwargs):
        if not self.slug:
            cible = self.engin if self.engin else self.remorque
            if cible:
                self.slug = self.generate_unique_slug(f"{cible.immatriculation}-{self.numero_serie}", Citerne.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        cible = self.engin if self.engin else self.remorque
        return f"Citerne {self.numero_serie} de {cible}" if cible else f"Citerne {self.numero_serie}"

    class Meta:
        ordering = ["numero_serie"]
        verbose_name = "Citerne"
        verbose_name_plural = "Citernes"

    def clean(self):
        super().clean()
        titres_fichiers = [f.titre.lower() for f in self.fichiers.all()]
        if "certificat jaugeage" not in titres_fichiers:
            raise ValidationError({'fichiers': "Le certificat de jaugeage est obligatoire pour cette citerne."})
