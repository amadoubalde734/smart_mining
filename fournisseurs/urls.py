# fournisseurs/urls.py
from django.urls import path
from . import views

app_name = 'fournisseurs'

urlpatterns = [
    # Fournisseurs
    path('', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('ajouter/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('<slug:slug>/', views.detail_fournisseur, name='detail_fournisseur'),
    path('<slug:slug>/modifier/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('<slug:slug>/supprimer/', views.supprimer_fournisseur, name='supprimer_fournisseur'),

    # Contacts fournisseurs
    path('<slug:slug>/contacts/', views.liste_contacts, name='liste_contacts'),
    path('<slug:slug>/contacts/ajouter/', views.ajouter_contact, name='ajouter_contact'),
    path('contacts/<int:pk>/modifier/', views.modifier_contact, name='modifier_contact'),
    path('contacts/<int:pk>/supprimer/', views.supprimer_contact, name='supprimer_contact'),
]
