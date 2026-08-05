
# notifications/models.py
from django.conf import settings
from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)  # Ajouter un titre clair pour la notification
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True, null=True)  # URL pour le bouton "Consulter"
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    etape = models.CharField(max_length=50, blank=True, null=True)  # Étape du risque associée

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"


# risks/models.py
from django.db import models

class ParametrageRapport(models.Model):
    statuts = models.JSONField(default=list, blank=True)       # Statuts de risque à notifier
    roles_en_copie = models.JSONField(default=list, blank=True) # Rôles à mettre en copie
    jours_avant = models.PositiveIntegerField(default=1)       # Nombre de jours avant notification
    actif = models.BooleanField(default=True)                  # Permet d’activer/désactiver ce paramétrage

    def __str__(self):
        return f"Paramétrage Rapport (jours_avant={self.jours_avant}, actif={self.actif})"
