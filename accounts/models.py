from django.contrib.auth.models import AbstractUser
from django.db import models
from parametrage.models import Societe, Ville, Site


class CustomUser(AbstractUser):
    # --------------------------
    # Rôle unique : Administrateur
    # --------------------------
    ROLE_ADMIN = 'administrateur'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrateur Système'),
    ]

    id = models.AutoField(primary_key=True)
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=ROLE_ADMIN,
        verbose_name="Rôle utilisateur"
    )

    # --------------------------
    # Informations personnelles
    # --------------------------
    ville = models.ForeignKey(Ville, blank=True, null=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, blank=True, null=True, on_delete=models.SET_NULL)
    contact = models.CharField(max_length=191, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    id_societe = models.ForeignKey(Societe, blank=True, null=True, on_delete=models.SET_NULL)

    # --------------------------
    # Statuts
    # --------------------------
    statut_compte = models.BooleanField(default=True)
    statut_connecte = models.BooleanField(default=False)
    statut_log = models.BooleanField(default=True)
    statut_change_pass = models.BooleanField(default=False)
    statut_d = models.BooleanField(default=True)

    # --------------------------
    # Sécurité / Réinitialisation
    # --------------------------
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_expiry = models.DateTimeField(blank=True, null=True)

    # --------------------------
    # Groupes et permissions
    # --------------------------
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='Groupes de l’utilisateur.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Permissions spécifiques à l’utilisateur.'
    )

    # --------------------------
    # Représentation
    # --------------------------
    def __str__(self):
        full_name = self.get_full_name()
        return f"{self.username} ({full_name})" if full_name else self.username

    # --------------------------
    # Méthode utilitaire
    # --------------------------
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['username']
