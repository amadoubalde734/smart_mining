from django.urls import path
from . import views

app_name = 'habilitation'

urlpatterns = [

    # ===============================
    # DASHBOARD HABILITATION
    # ===============================
     path('dashboard_habilitation/', views.dashboard_habilitation, name='dashboard_habilitation'),

    # ===============================
    # IDENTIFICATION EMPLOYE
    # ===============================
    # path('identifications/', views.identification_list, name='identification_list'),
    # path('identifications/ajouter/', views.identification_create, name='identification_create'),
    # path('identifications/<slug:slug>/modifier/', views.identification_update, name='identification_update'),
    # path('identifications/<slug:slug>/supprimer/', views.identification_delete, name='identification_delete'),

    # ===============================
    # FORMATION CHAUFFEUR
    # ===============================
    path('formations/', views.formation_list, name='formation_list'),
    path('formations/ajouter/', views.formation_create, name='formation_create'),
    path('formations/<slug:slug>/modifier/', views.formation_update, name='formation_update'),
    path('formations/<slug:slug>/supprimer/', views.formation_delete, name='formation_delete'),

    # ===============================
    # SUIVI PASS MINE (support fichiers joints)
    # ===============================
    path("pass/", views.pass_list, name="pass_list"),
    path("pass/ajouter/", views.pass_create, name="pass_create"),
    path("pass/<slug:slug>/modifier/", views.pass_update, name="pass_update"),
    path("pass/<slug:slug>/supprimer/", views.pass_delete, name="pass_delete"),

    # ===============================
    # PERMIS DE TRAVAIL (support fichiers joints)
    # ===============================
    path('permis/', views.permis_list, name='permis_list'),
    path('permis/ajouter/', views.permis_create, name='permis_create'),
    path('permis/<slug:slug>/modifier/', views.permis_update, name='permis_update'),
    path('permis/<slug:slug>/supprimer/', views.permis_delete, name='permis_delete'),

    # ===============================
    # COMPORTEMENT ET CONDUITE
    # ===============================
    path('conduite/', views.conduite_list, name='conduite_list'),
    path('conduite/ajouter/', views.conduite_create, name='conduite_create'),
    path('conduite/<slug:slug>/modifier/', views.conduite_update, name='conduite_update'),
    path('conduite/<slug:slug>/supprimer/', views.conduite_delete, name='conduite_delete'),

    # habilitation/urls.py
    path('historiques/', views.historique_list, name='historique_list'),

]
