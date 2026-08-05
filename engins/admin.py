from django.contrib import admin
from .models import (
    TypeEngin, CategorieEngin, Marque, Modele, StatutEngin, SiteEngin,
     Remorque, Citerne, AssuranceEngin, VignetteConformite,
     ControleTechnique
)
from engins.models.evenements import TypeEvenement

# ===============================
# TYPES EVENEMENTS
# ===============================
@admin.register(TypeEvenement)
class TypeEvenementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom',)
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('nom',)

# ===============================
# TYPES D'ENGINS
# ===============================
@admin.register(TypeEngin)
class TypeEnginAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom',)
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('nom',)

# ===============================
# CATEGORIES D'ENGINS
# ===============================
@admin.register(CategorieEngin)
class CategorieEnginAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom',)
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('nom',)

# ===============================
# MARQUES
# ===============================
@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom',)
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('nom',)

# ===============================
# MODELES
# ===============================
@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque', 'type_engin', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif', 'type_engin', 'marque')
    search_fields = ('nom', 'marque__nom', 'type_engin__nom')
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('marque', 'nom')

# ===============================
# STATUTS ENGINS
# ===============================
@admin.register(StatutEngin)
class StatutEnginAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom',)
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('nom',)

# ===============================
# SITES / DEPOTS
# ===============================
@admin.register(SiteEngin)
class SiteEnginAdmin(admin.ModelAdmin):
    list_display = ('nom_site', 'adresse', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom_site', 'adresse')
    prepopulated_fields = {"slug": ("nom_site",)}
    ordering = ('nom_site',)

# ===============================
# REMORQUES
# ===============================
@admin.register(Remorque)
class RemorqueAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'tracteur', 'type_remorque', 'actif', 'created_at', 'updated_at')
    list_filter = ('type_remorque', 'actif')
    search_fields = ('immatriculation', 'tracteur__immatriculation')
    prepopulated_fields = {"slug": ("immatriculation",)}
    ordering = ('immatriculation',)

# ===============================
# CITERNES
# ===============================
@admin.register(Citerne)
class CiterneAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'engin', 'remorque', 'volume', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('numero_serie', 'engin__immatriculation', 'remorque__immatriculation')
    prepopulated_fields = {"slug": ("numero_serie",)}
    ordering = ('numero_serie',)

# ===============================
# ASSURANCES
# ===============================
@admin.register(AssuranceEngin)
class AssuranceEnginAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_assurance', 'engin', 'date_debut', 'date_fin', 'actif')
    list_filter = ('type_assurance', 'actif')
    search_fields = ('nom', 'engin__immatriculation')
    ordering = ('-date_fin',)

# ===============================
# VIGNETTES
# ===============================
@admin.register(VignetteConformite)
class VignetteConformiteAdmin(admin.ModelAdmin):
    list_display = ('engin', 'type_vignette', 'date_emission', 'date_expire', 'actif')
    list_filter = ('type_vignette', 'actif')
    search_fields = ('engin__immatriculation',)
    ordering = ('-date_expire',)


# ===============================
# CONTROLES TECHNIQUES
# ===============================
@admin.register(ControleTechnique)
class ControleTechniqueAdmin(admin.ModelAdmin):
    list_display = ('engin', 'date_controle', 'resultat', 'en_validite')
    list_filter = ('resultat', 'en_validite')
    search_fields = ('engin__immatriculation',)
    ordering = ('-date_controle',)
