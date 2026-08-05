from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from notifications.models import Notification
from parametrage.utils import get_email_config

import logging
import re
import traceback

logger = logging.getLogger(__name__)

def strip_html_tags(html):
    """Nettoie le HTML pour en faire une version texte simple."""
    clean_text = re.sub('<[^<]+?>', '', html)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text


def send_notification_and_email(users, subject, message_html):
    """
    Envoie une notification interne et un email à une liste d'utilisateurs actifs.
    """
    try:
        active_users = [user for user in users if user.is_active]
        if not active_users:
            logger.info("Aucun utilisateur actif pour envoyer la notification.")
            return

        # Charger la configuration email depuis la base
        email_config = get_email_config()
        if not email_config:
            logger.error("Configuration email introuvable ou incomplète.")
            return

        # Connexion SMTP personnalisée
        try:
            connection = get_connection(
                backend=email_config['EMAIL_BACKEND'],
                host=email_config['EMAIL_HOST'],
                port=email_config['EMAIL_PORT'],
                username=email_config['EMAIL_HOST_USER'],
                password=email_config['EMAIL_HOST_PASSWORD'],
                use_tls=email_config['EMAIL_USE_TLS'],
            )
        except Exception as smtp_error:
            logger.error(f"Erreur lors de la création de la connexion SMTP : {smtp_error}")
            logger.debug(traceback.format_exc())
            return

        notifications = []

        for user in active_users:
            # Rendu du message personnalisé pour chaque utilisateur
            full_message_html = render_to_string(
                'backend/notifications/notifications_email.html',
                {
                    'message': message_html,
                    'user': user,
                }
            )

            # Enregistrement notification interne
            notifications.append(Notification(
                user=user,
                message=full_message_html,
            ))

            # Envoi email
            if user.email:
                try:
                    text_fallback = strip_html_tags(full_message_html)
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=text_fallback,
                        from_email=email_config['DEFAULT_FROM_EMAIL'],
                        to=[user.email],
                        connection=connection,
                    )
                    email.attach_alternative(full_message_html, "text/html")
                    email.send()
                except Exception as email_error:
                    logger.error(f"Erreur lors de l'envoi d'email à {user.email} : {email_error}")
                    logger.debug(traceback.format_exc())

        # Création groupée des notifications internes
        Notification.objects.bulk_create(notifications)

    except Exception as e:
        logger.error(f"Erreur générale lors de l'envoi de notifications/email : {e}")
        logger.debug(traceback.format_exc())
