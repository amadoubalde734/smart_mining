from django.db import models
from django.utils.text import slugify
import uuid

# -----------------------
# Mixins
# -----------------------
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
    class Meta:
        abstract = True

    def generate_unique_slug(self, field_value, queryset):
        base_slug = slugify(field_value)
        slug = base_slug
        counter = 1
        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

# -----------------------
# Fournisseur
# -----------------------
class Fournisseur(TimeStampedModel, StatusModel, SlugModel):
    numero_fournisseur = models.CharField(max_length=50, unique=True)
    nom_societe = models.CharField(max_length=150)
    motif_creation = models.TextField(blank=True, null=True)
    societe_concernee = models.CharField(max_length=150, blank=True, null=True)
    forme_juridique = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    activite = models.TextField(blank=True, null=True)
    # Banques et informations légales gardées comme avant

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(f"{self.nom_societe}-{self.numero_fournisseur}", Fournisseur.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_societe} ({self.numero_fournisseur})"

    class Meta:
        ordering = ['nom_societe']
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        indexes = [
            models.Index(fields=['nom_societe']),
            models.Index(fields=['numero_fournisseur']),
        ]

# -----------------------
# Contact Fournisseur
# -----------------------
class ContactFournisseur(TimeStampedModel, StatusModel):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='contacts')
    nom = models.CharField(max_length=150)
    fonction = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)

    TYPE_CONTACT_CHOICES = [
        ('commercial', 'Responsable Commercial'),
        ('comptabilite', 'Comptabilité'),
        ('commande', 'Contact Commande'),
        ('autre', 'Autre'),
    ]
    type_contact = models.CharField(max_length=20, choices=TYPE_CONTACT_CHOICES, default='autre')

    def __str__(self):
        return f"{self.nom} ({self.get_type_contact_display()})"

    class Meta:
        ordering = ['nom']
        verbose_name = "Contact Fournisseur"
        verbose_name_plural = "Contacts Fournisseur"
