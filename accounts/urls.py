from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    RegistrationView, VerificationView,
    UsernameValidationView, EmailValidationView,
    AdminLoginView, FrontLoginView, LogoutView,
    AddUserView, ChangeUserPasswordView, ResetCodeView,
    ListUsersView, DeleteUserView, ConnectedUsersView,
    ResetPasswordWithCodeView, EditUserView
)

app_name = 'accounts'

urlpatterns = [
    # FRONT-END
    path('front/register/', RegistrationView.as_view(), name="front_register"),
    path('front/login/', FrontLoginView.as_view(), name="front_login"),
    path('front/logout/', LogoutView.as_view(), name='front_logout'),

    # ADMIN
    path('register/', RegistrationView.as_view(), name="admin_register"),
    path('login/', AdminLoginView.as_view(), name="admin_login"),
    path('logout/', LogoutView.as_view(), name='admin_logout'),

    # Activation compte
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name="activate"),

    # Validation AJAX
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),

    # Gestion utilisateurs
    path('add_user/', AddUserView.as_view(), name='add_user'),
    path('edit-user/<int:user_id>/', EditUserView.as_view(), name='edit_user'),
    path('connected-users/', ConnectedUsersView.as_view(), name='connected_users'),
    path('list-users/', ListUsersView.as_view(), name='list_users'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),

    # Mot de passe
    path('request-reset-code/', ResetCodeView.as_view(), name='request_reset_code'),
    path('reset-password/<int:user_id>/', ResetPasswordWithCodeView.as_view(), name='reset_code_verify'),
    path('change-password/<int:user_id>/', ChangeUserPasswordView.as_view(), name='change_user_password'),
    path('reset-code/', ResetCodeView.as_view(), name="reset_code"),
]
