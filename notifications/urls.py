from django.urls import path
from . import views

app_name = 'notifications'  # Définir le namespace

urlpatterns = [
    path('', views.notification_view, name='notification_list'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('clear-all/', views.clear_all, name='clear_all'),  # Ajouter cette ligne pour le "Clear All"
]
