from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'id_societe', 'statut_compte', 'statut_connecte', 'is_staff')
    list_filter = ('role', 'statut_compte', 'is_staff', 'id_societe')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'contact')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'contact', 'ville', 'avatar')
        }),
        ('Statut & horaires', {
            'fields': (
                'statut_compte', 'statut_connecte', 'statut_change_pass',
                'statut_log', 'statut_d', 'debloqueur'
            )
        }),
        ('Société et rôle', {
            'fields': ('id_societe', 'role')
        }),
        ('Dates et heures', {
            'fields': ('heure_debut', 'heure_fin', 'date_observ', 'date_derog', 'date_debloc')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

# 🎨 Personnalisation de l’en-tête de l’admin (s'affiche aussi dans Jazzmin)
admin.site.site_header = "Administration du Personnel"
admin.site.site_title = "Interface d'administration"
admin.site.index_title = "Bienvenue dans la gestion des utilisateurs"
