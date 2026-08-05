from django.contrib import admin

# Register your models here.
# parametrage/admin.py
from django.contrib import admin
from .models import Societe, Ville, Site, Departement, Service, Fonction, EmailSettings, Tva

# ===============================
# SOCIETES
# ===============================
@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'date_integration', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('libelle',)
    prepopulated_fields = {"slug": ("libelle",)}
    ordering = ('libelle',)

# ===============================
# VILLES
# ===============================
@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'pays', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif', 'pays')
    search_fields = ('libelle', 'pays')
    prepopulated_fields = {"slug": ("libelle",)}
    ordering = ('libelle',)

# ===============================
# SITES
# ===============================
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('nom_site', 'adresse', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom_site', 'adresse')
    prepopulated_fields = {"slug": ("nom_site",)}
    ordering = ('nom_site',)

# ===============================
# DEPARTEMENTS
# ===============================
@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom',)
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('nom',)

# ===============================
# SERVICES
# ===============================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'departement', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif', 'departement')
    search_fields = ('nom', 'departement__nom')
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('departement', 'nom')

# ===============================
# FONCTIONS
# ===============================
@admin.register(Fonction)
class FonctionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'service', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif', 'service')
    search_fields = ('nom', 'service__nom')
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ('service', 'nom')

# ===============================
# EMAIL SETTINGS
# ===============================
@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('email_host', 'email_port', 'email_host_user', 'email_use_tls')
    search_fields = ('email_host', 'email_host_user')

# ===============================
# TVA
# ===============================
@admin.register(Tva)
class TvaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'taux', 'code', 'actif', 'par_defaut', 'created_at', 'updated_at')
    list_filter = ('actif', 'par_defaut')
    search_fields = ('nom', 'code')
    ordering = ('nom',)
