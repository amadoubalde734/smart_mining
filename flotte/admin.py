# Register your models here.
# flotte/admin.py
from django.contrib import admin
from .models import Flotte

# ===============================
# ADMIN FLOTTES
# ===============================
@admin.register(Flotte)
class FlotteAdmin(admin.ModelAdmin):
    # Champs affichés dans la liste
    list_display = ('nom', 'site', 'actif', 'created_at', 'updated_at')
    
    # Filtres sur la droite
    list_filter = ('actif', 'site')
    
    # Champs sur lesquels faire une recherche
    search_fields = ('nom', 'description', 'site__nom_site')
    
    # Champs à préremplir automatiquement (slug)
    prepopulated_fields = {"slug": ("nom",)}
    
    # Ordre par défaut
    ordering = ('nom',)
    
    # Champs ManyToMany affichés avec un widget vertical pratique
    filter_horizontal = ('engins',)
