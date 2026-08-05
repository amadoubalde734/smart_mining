from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from accounts.models import CustomUser
from risks.models import ActionSuivi
from notifications.models import ParametrageRapport
from notifications.utils import send_notification_and_email


@shared_task
def envoyer_rapports_actions_suivi():
    # Récupérer la configuration, sinon valeurs par défaut
    config = ParametrageRapport.objects.first()

    statuts = config.statuts if config and config.statuts else ["non_demarree", "en_cours", "prévue"]
    roles_copie = config.roles_en_copie if config and config.roles_en_copie else [
        CustomUser.ROLE_QSE_TEAM,
        CustomUser.ROLE_TOP_MANAGEMENT,
        CustomUser.ROLE_ADMIN,
        CustomUser.ROLE_RESPONSABLE_PROCESSUS,
    ]
    jours_avant = config.jours_avant if config and config.jours_avant is not None else 1

    today = timezone.localdate()  # Prendre la date locale (sans l'heure)
    jours_cibles = [today + timedelta(days=i) for i in range(jours_avant + 1)]

    # Filtrer les actions selon le statut et les dates ciblées
    actions = ActionSuivi.objects.filter(
        statut_action__in=statuts
    ).filter(
        Q(date_debut_actions__in=jours_cibles) |
        Q(date_fin_actions__in=jours_cibles) |
        Q(date_prevue_verification__in=jours_cibles)
    ).distinct()

    # Récupérer en une requête les utilisateurs en copie actifs
    copie_users = CustomUser.objects.filter(role__in=roles_copie, is_active=True)

    for action in actions:
        destinataires = set()

        if action.responsable and action.responsable.is_active:
            destinataires.add(action.responsable)

        # Ajouter les utilisateurs en copie
        destinataires.update(copie_users)

        # Préparer le message (vérifier si 'risque' existe)
        intitule_risque = getattr(action.risque, "intitule_description", "Non défini")

        message = (
            f"🔔 Rappel sur une action de suivi liée au risque : {intitule_risque}\n"
            f"- 📅 Démarrage prévu : {action.date_debut_actions}\n"
            f"- ✅ Réalisation prévue : {action.date_fin_actions}\n"
            f"- 🔍 Vérification prévue : {action.date_prevue_verification}\n"
            f"- 👤 Responsable : {action.responsable.get_full_name() if action.responsable else 'Non défini'}\n"
            "\nVeuillez vérifier l'avancement ou mettre à jour la fiche."
        )

        send_notification_and_email(list(destinataires), "⚠️ Rappel Action de Suivi", message)
