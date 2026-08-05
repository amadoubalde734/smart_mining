from django.urls import path
from . import views

app_name = 'flotte'

urlpatterns = [
    
    # # ===============================
    # # SUIVI PRODUCTION
    # # ===============================
    # path('suivis/', views.suivi_list, name='suivi_production'),
    # path('suivis/ajouter/', views.suivi_create, name='suivi_create'),
    # path('suivis/<int:pk>/modifier/', views.suivi_update, name='suivi_update'),
    # path('suivis/<int:pk>/supprimer/', views.suivi_delete, name='suivi_delete'),

    # ===============================
    # FLOTTES
    # ===============================
    path('', views.flotte_list, name='flotte_list'),
    path('<slug:slug>/modifier/', views.flotte_update, name='flotte_update'),
    path('<slug:slug>/supprimer/', views.flotte_delete, name='flotte_delete'),
    path('<slug:slug>/', views.flotte_detail, name='flotte_detail'),
]
