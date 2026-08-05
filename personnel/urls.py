from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    # ===============================
    # EMPLOYÉS CRUD
    # ===============================
    path('employes/', views.employe_list, name='employe_list'),
    path('employes/ajouter/', views.employe_create, name='employe_create'),
    path('employes/<slug:slug>/modifier/', views.employe_update, name='employe_update'),
    path('employes/<slug:slug>/supprimer/', views.employe_delete, name='employe_delete'),
    path('employe_dashboard/', views.employe_dashboard, name='employe_dashboard'),

    path('profil/<slug:slug>/', views.employe_profil, name='employe_profil'),
    path('historique/<slug:slug>/', views.employe_historique, name='employe_historique'),

    # ===============================
    # AJAX
    # ===============================
    path('ajax/services/', views.get_services_by_departement, name='ajax_services'),
    path('ajax/fonctions/', views.get_fonctions_by_service, name='get_fonctions_by_service'),  # <-- Nouvelle URL
]
