# utils/email_config.py (ou autre endroit à part)
from parametrage.models import EmailSettings

def get_email_config():
    settings = EmailSettings.objects.first()
    if not settings:
        # Valeurs par défaut si rien en base
        return {
            'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
            'EMAIL_HOST': 'smtp.gmail.com',
            'EMAIL_PORT': 587,
            'EMAIL_USE_TLS': True,
            'EMAIL_HOST_USER': '',
            'EMAIL_HOST_PASSWORD': '',
            'DEFAULT_FROM_EMAIL': '',
        }
    return {
        'EMAIL_BACKEND': settings.email_backend,
        'EMAIL_HOST': settings.email_host,
        'EMAIL_PORT': settings.email_port,
        'EMAIL_USE_TLS': settings.email_use_tls,
        'EMAIL_HOST_USER': settings.email_host_user,
        'EMAIL_HOST_PASSWORD': settings.email_host_password,
        'DEFAULT_FROM_EMAIL': settings.default_from_email,
    }
