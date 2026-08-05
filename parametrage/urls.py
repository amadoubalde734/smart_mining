from django.urls import path
from . import views

app_name = 'parametrage'

urlpatterns = [
    # ============================
    # SOCIETES
    # ============================
    path('societes/', views.ajouter_societe, name='ajouter_societe'),
    path('societes/modifier/<int:pk>/', views.modifier_societe, name='modifier_societe'),
    path('societes/supprimer/<int:pk>/', views.supprimer_societe, name='supprimer_societe'),
    path('societes/liste/', views.liste_societes, name='liste_societes'),

    # ============================
    # VILLES
    # ============================
    path('villes/', views.ajouter_ville, name='ajouter_ville'),
    path('villes/modifier/<int:pk>/', views.modifier_ville, name='modifier_ville'),
    path('villes/supprimer/<int:pk>/', views.supprimer_ville, name='supprimer_ville'),
    path('villes/liste/', views.liste_villes, name='liste_villes'),

    # ============================
    # SITES
    # ============================
    path('sites/', views.ajouter_site, name='ajouter_site'),
    path('sites/modifier/<int:pk>/', views.modifier_site, name='modifier_site'),
    path('sites/supprimer/<int:pk>/', views.supprimer_site, name='supprimer_site'),
    path('sites/liste/', views.liste_sites, name='liste_sites'),

    # ============================
    # DEPARTEMENTS
    # ============================
    path('departements/liste/', views.liste_departements, name='liste_departements'),
    path('departements/ajouter/', views.ajouter_departement, name='ajouter_departement'),
    path('departements/modifier/<int:pk>/', views.modifier_departement, name='modifier_departement'),
    path('departements/supprimer/<int:pk>/', views.supprimer_departement, name='supprimer_departement'),
    path('departements/toggle/<int:pk>/', views.toggle_departement, name='toggle_departement'),


    # ============================
    # SERVICES
    # ============================
    path('services/', views.ajouter_service, name='ajouter_service'),
    path('services/modifier/<int:pk>/', views.modifier_service, name='modifier_service'),
    path('services/supprimer/<int:pk>/', views.supprimer_service, name='supprimer_service'),
    path('services/liste/', views.liste_services, name='liste_services'),

    # ============================
    # FONCTIONS
    # ============================
    path('fonctions/', views.ajouter_fonction, name='ajouter_fonction'),
    path('fonctions/modifier/<int:pk>/', views.modifier_fonction, name='modifier_fonction'),
    path('fonctions/supprimer/<int:pk>/', views.supprimer_fonction, name='supprimer_fonction'),
    path('fonctions/liste/', views.liste_fonctions, name='liste_fonctions'),

    # ============================
    # EMAIL SETTINGS (optionnel)
    # ============================
    # path('email-settings/', views.email_settings, name='email_settings'),
]
