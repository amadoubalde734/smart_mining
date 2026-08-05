from django.urls import path, include
from . import views
# from accounts.views import FrontLoginView as LoginView, RegistrationView, LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    # path('pages/about/', views.about, name='about'),
    # path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    
    # # Authentification front
    # # path('login/', LoginView.as_view(), name='front_login'),
    # # path('logout/', LogoutView.as_view(), name='front_logout'),
    # # path('register/', RegistrationView.as_view(), name='front_register'),

    # # Inclusion des modules QSE360 avec namespaces
    
]
