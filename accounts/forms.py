from django import forms
from django.contrib.auth.forms import PasswordChangeForm


from django import forms
from django.contrib.auth.forms import SetPasswordForm
from .models import CustomUser

class CustomPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Nouveau mot de passe"})
    )
    new_password2 = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirmation du mot de passe"})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({"class": "form-control", "placeholder": "Nouveau mot de passe"})
        self.fields['new_password2'].widget.attrs.update({"class": "form-control", "placeholder": "Confirmation du mot de passe"})


# accounts/forms.py
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from .models import CustomUser

# ----------------------------------------
# Formulaire pour demander le code de réinitialisation
# ----------------------------------------
class RequestResetCodeForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez votre email"
        })
    )

# ----------------------------------------
# Formulaire pour réinitialiser le mot de passe avec code
# ----------------------------------------
class ResetPasswordWithCodeForm(SetPasswordForm):
    code = forms.CharField(
        label="Code de réinitialisation",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({"class": "form-control"})
        self.fields['new_password2'].widget.attrs.update({"class": "form-control"})
