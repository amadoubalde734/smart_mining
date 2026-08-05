from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from accounts.models import CustomUser
from notifications.utils import send_notification_and_email


# -----------------------------
# FONCTIONS UTILITAIRES GÉNÉRIQUES
# -----------------------------
def send_generic_notification(recipients, subject, message_html):
    """Envoie une notification interne et un email après le commit de la transaction."""
    transaction.on_commit(lambda: send_notification_and_email(recipients, subject, message_html))


# -----------------------------
# EXEMPLE DE SIGNAL GÉNÉRIQUE
# -----------------------------
# 💡 Tu pourras copier ce bloc pour n’importe quel modèle
#    en changeant simplement `sender=TonModele` et le contenu du message.
@receiver(post_save)
def notification_generique(sender, instance, created, **kwargs):
    """
    Exemple de signal générique.
    À personnaliser selon le modèle concerné.
    """
    try:
        # Exemple d’auteur
        auteur = getattr(instance, 'cree_par', None)
        auteur_nom = auteur.get_full_name() if auteur else 'Un utilisateur'

        # Message et sujet
        if created:
            subject = f"Nouveau {sender.__name__} créé"
            message_html = mark_safe(f"<p>{auteur_nom} a créé un nouvel enregistrement ({sender.__name__}).</p>")
        else:
            subject = f"{sender.__name__} mis à jour"
            message_html = mark_safe(f"<p>{auteur_nom} a mis à jour un enregistrement ({sender.__name__}).</p>")

        # Détermination des destinataires (exemple : administrateurs)
        recipients = CustomUser.objects.filter(role=CustomUser.ROLE_ADMIN, is_active=True)

        # Envoi de la notification
        send_generic_notification(recipients, subject, message_html)

    except Exception as e:
        import logging, traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur lors de la notification du modèle {sender.__name__} : {e}")
        logger.debug(traceback.format_exc())
