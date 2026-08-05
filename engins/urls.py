from django.urls import path
from . import views

app_name = 'engins'

urlpatterns = [

    # ===============================
    # DASHBOARD ENGINS
    # ===============================
    path('dashboard_engins/', views.dashboard_engins, name='dashboard_engins'),


    # ===============================
    # TYPES D'ENGINS
    # ===============================
    path('types/', views.type_list, name='type_list'),
    path('types/ajouter/', views.type_create, name='type_create'),
    path('types/modifier/<slug:slug>/', views.type_update, name='type_update'),
    path('types/supprimer/<slug:slug>/', views.type_delete, name='type_delete'),

    # ===============================
    # CATEGORIES D'ENGINS
    # ===============================
    path('categories/', views.categorie_list, name='categorie_list'),
    path('categories/ajouter/', views.categorie_create, name='categorie_create'),
    path('categories/modifier/<slug:slug>/', views.categorie_update, name='categorie_update'),
    path('categories/supprimer/<slug:slug>/', views.categorie_delete, name='categorie_delete'),

    # ===============================
    # MARQUES ET MODELES
    # ===============================
    path('marques/', views.marque_list, name='marque_list'),
    path('marques/ajouter/', views.marque_create, name='marque_create'),
    path('marques/modifier/<slug:slug>/', views.marque_update, name='marque_update'),
    path('marques/supprimer/<slug:slug>/', views.marque_delete, name='marque_delete'),

    # ===============================
    # MODELES
    # ===============================
    path('modeles/', views.modele_list, name='modele_list'),
    path('modeles/ajouter/', views.modele_create, name='modele_create'),
    path('modeles/<slug:slug>/modifier/', views.modele_update, name='modele_update'),
    path('modeles/<slug:slug>/supprimer/', views.modele_delete, name='modele_delete'),

    # ===============================
    # STATUTS ENGINS
    # ===============================
    path('statuts/', views.statut_list, name='statut_list'),
    path('statuts/ajouter/', views.statut_create, name='statut_create'),
    path('statuts/modifier/<slug:slug>/', views.statut_update, name='statut_update'),
    path('statuts/supprimer/<slug:slug>/', views.statut_delete, name='statut_delete'),

    # ===============================
    # SITES / DEPOTS
    # ===============================
    path('sites/', views.site_list, name='site_list'),
    path('sites/ajouter/', views.site_create, name='site_create'),
    path('sites/modifier/<slug:slug>/', views.site_update, name='site_update'),
    path('sites/supprimer/<slug:slug>/', views.site_delete, name='site_delete'),

    # ===============================
    # ENGINS
    # ===============================
    path('engins/', views.engin_list, name='engin_list'),
    path('engins/ajouter/', views.engin_create, name='engin_create'),
    path('engins/modifier/<slug:slug>/', views.engin_update, name='engin_update'),
    path('engins/supprimer/<slug:slug>/', views.engin_delete, name='engin_delete'),

    # ===============================
    # INSPECTIONS ENGINS
    path('inspections/nouvelle/', views.inspection_create, name='inspection_create'),
    path('inspections/liste/', views.inspection_list, name='inspection_list'),
    path('inspections/<slug:slug>/', views.inspection_detail, name='inspection_detail'),
    path('inspections/<slug:slug>/modifier/', views.inspection_update, name='inspection_update'),
    path('inspections/<slug:slug>/supprimer/', views.inspection_delete, name='inspection_delete'),


    # -------------------------------
    # PAGE PRINCIPALE DOCUMENTS LEGAUX
    # -------------------------------
    path('documents-legaux/', views.documents_legaux, name='documents_legaux'),

    # ===============================
    # ASSURANCES
    # ===============================
    path('assurances/', views.assurance_list, name='assurances'),
    path('assurances/<int:pk>/modifier/', views.assurance_update, name='assurance_update'),
    path('assurances/<int:pk>/supprimer/', views.assurance_delete, name='assurance_delete'),

    # ===============================
    # VIGNETTES
    # ===============================
    path('vignettes/', views.vignettes_list, name='vignettes'),
    path('vignettes/<int:pk>/modifier/', views.vignette_update, name='vignette_update'),
    path('vignettes/<int:pk>/supprimer/', views.vignette_delete, name='vignette_delete'),

    # ===============================
    # CONTROLES TECHNIQUES
    # ===============================
    path('controles/', views.controles_list, name='controle_technique'),
    path('controles/ajouter/', views.controle_create, name='controle_create'),
    path('controles/<int:pk>/modifier/', views.controle_update, name='controle_update'),
    path('controles/<int:pk>/supprimer/', views.controle_delete, name='controle_delete'),

    # ===============================
    # CERTIFICATS DE JAUGEAGE
    # ===============================
    path('certificats-jaugeage/', views.certificat_jaugeage_list, name='certificat_jaugeage_list'),  # si tu veux une liste
    path('certificats-jaugeage/ajouter/', views.certificat_jaugeage_create, name='certificat_jaugeage_create'),
    path('certificats-jaugeage/<int:pk>/modifier/', views.certificat_jaugeage_update, name='certificat_jaugeage_update'),
    path('certificats-jaugeage/<int:pk>/supprimer/', views.certificat_jaugeage_delete, name='certificat_jaugeage_delete'),

    # ===============================
    # CARTES GRISES
    # ===============================
    path('cartes-grises/', views.carte_grise_list, name='carte_grise_list'),  # liste des cartes grises
    path('cartes-grises/ajouter/', views.carte_grise_create, name='carte_grise_create'),  # création
    path('cartes-grises/<int:pk>/modifier/', views.carte_grise_update, name='carte_grise_update'),  # modification
    path('cartes-grises/<int:pk>/supprimer/', views.carte_grise_delete, name='carte_grise_delete'),  # suppression
        
    # ===============================
    # EVENEMENTS & INTERVENTIONS
    # ===============================

    # Liste des événements
    path('evenements/', views.evenement_list, name='evenement_list'),

    # Créer un nouvel événement
    path('evenements/ajouter/', views.evenement_create, name='evenement_create'),

    # Détail d'un événement
    path('evenements/<int:pk>/', views.evenement_detail, name='evenement_detail'),

    # Modifier un événement
    path('evenements/<int:pk>/modifier/', views.evenement_update, name='evenement_update'),

    # Supprimer un événement
    path('evenements/<int:pk>/supprimer/', views.evenement_delete, name='evenement_delete'),

    # Intervention associée à un événement (optionnel)
    # path('interventions/', views.intervention_list, name='intervention_list'),
    # path('interventions/ajouter/', views.intervention_create, name='intervention_create'),
    # path('interventions/<int:pk>/modifier/', views.intervention_update, name='intervention_update'),
    # path('interventions/<int:pk>/supprimer/', views.intervention_delete, name='intervention_delete'),

    
]
    