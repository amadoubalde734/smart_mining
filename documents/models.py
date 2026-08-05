from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
import os

# =========================
# Types de documents
# =========================
class DocumentType(models.Model):
    nom = models.CharField(max_length=100)  # ex: Carte Grise, Assurance, Photo, Permis...
    modele = models.CharField(max_length=50)  # ex: 'Engin', 'Employe', 'Medicament', etc.

    def __str__(self):
        return f"{self.nom} ({self.modele})"


# =========================
# Fichiers joints génériques
# =========================
def upload_to(instance, filename):
    """
    Organisation des fichiers par module/type de document
    """
    modele = instance.type_document.modele if instance.type_document else 'autre'
    # Nettoyer le nom de fichier
    filename_base, filename_ext = os.path.splitext(filename)
    filename_slug = slugify(filename_base)
    return f"fichiers_joints/{modele}/{filename_slug}{filename_ext.lower()}"

class FichierJoint(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    fichier = models.FileField(upload_to=upload_to)
    description = models.TextField(blank=True, null=True)
    type_document = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichiers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Champs pour la relation générique
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def save(self, *args, **kwargs):
        # Créer le slug automatiquement
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def clean(self):
        # Validation du fichier
        if self.fichier:
            if self.fichier.size > 5 * 1024 * 1024:
                raise ValidationError("Le fichier ne doit pas dépasser 5 Mo.")
            ext = os.path.splitext(self.fichier.name)[1][1:].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png', 'docx', 'xlsx']:
                raise ValidationError("Format de fichier non autorisé (pdf, jpg, jpeg, png, docx, xlsx).")

    def __str__(self):
        if self.type_document:
            return f"{self.type_document.nom} - {self.titre}"
        return self.titre
