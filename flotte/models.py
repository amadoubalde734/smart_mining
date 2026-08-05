# flotte/models.py
from django.db import models
from django.utils.text import slugify
import uuid
from engins.models import Engin, SiteEngin

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

        # boucle pour assurer l'unicité sans UUID long
        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    class Meta:
        abstract = True


# ===============================
# FLOTTES
# ===============================
class Flotte(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    site = models.ForeignKey(SiteEngin, on_delete=models.SET_NULL, null=True, blank=True)
    engins = models.ManyToManyField(Engin, related_name='flottes', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, Flotte.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Flotte"
        verbose_name_plural = "Flottes"


