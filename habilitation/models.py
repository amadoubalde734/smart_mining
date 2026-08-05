# habilitation/models.py
from django.db import models
from django.utils.text import slugify
import uuid
from personnel.models import Employe
from django.contrib.contenttypes.fields import GenericRelation
from documents.models import FichierJoint
import secrets
from parametrage.models import Site,Service
from flotte.models import Flotte
from datetime import datetime, date, timedelta
from engins.models import CategorieEngin


# ===============================
# MIXINS REUTILISABLES
# ===============================
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    actif = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(max_length=191, unique=True, blank=True)

    def generate_unique_slug(self, field_value, queryset):
        base_slug = slugify(field_value)
        slug = base_slug
        counter = 1
        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    class Meta:
        abstract = True

# ===============================
# Modèle pour les types de formation
# ===============================
class TypeFormation(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, TypeFormation.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Type de Formation"
        verbose_name_plural = "Types de Formations"

# ===============================
# Formation Chauffeur ERP-ready
# ===============================
class FormationChauffeur(TimeStampedModel, StatusModel, SlugModel):

    # --- Employé ---
    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name='formations_chauffeur'
    )

    # --- Encadrement ---
    formateur = models.ForeignKey(
        Employe,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='formations_donnees',
        verbose_name="Formateur"
    )

    # --- Références ---
    type_formation = models.ForeignKey(
        TypeFormation,
        on_delete=models.CASCADE,
        related_name='formations'
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="formations",
        verbose_name="Site de formation"
    )

    flotte = models.ForeignKey(
        Flotte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ✅ Catégorie liée aux engins
    categorie_engin = models.ForeignKey(
        CategorieEngin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Catégorie d'engin"
    )

    # --- Détails formation ---
    motif_theme = models.CharField(
        max_length=255,
        verbose_name="Motif / Thème"
    )

    date_formation = models.DateField(
        verbose_name="Date de réalisation"
    )

    duree_jours = models.PositiveIntegerField(default=1)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)

    organisme = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # --- Qualification ---
    QUALIFICATION_CHOICES = [
        ('Chauffeur PL', 'Chauffeur PL'),
        ('Chauffeur VL', 'Chauffeur VL'),
        ('Chauffeur', 'Chauffeur'),
        # tu peux ajouter d'autres types si besoin
    ]

    qualification_actuelle = models.CharField(
        max_length=50,  # suffisant pour ces valeurs
        choices=QUALIFICATION_CHOICES,
        verbose_name="Qualification actuelle"
    )

    # --- Évaluation ---
    NOTE_CHOICES = [(i, i) for i in range(0, 55)]
    note = models.PositiveSmallIntegerField(choices=NOTE_CHOICES)

    APPRECIATION_CHOICES = [
        ('Insuffisant', 'Insuffisant'),
        ('Passable', 'Passable'),
        ('Bien', 'Bien'),
        ('Très bien', 'Très bien'),
        ('Excellent', 'Excellent'),
    ]
    appreciation = models.CharField(
        max_length=20,
        choices=APPRECIATION_CHOICES
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    NOMBRE_FORMATION_CHOICES = [
    ('1', '1ère Formation'),
    ('2', '2ème Formation'),
    ('3', '3ème Formation'),
    ]

    nombre_formation = models.CharField(
        max_length=2,
        choices=NOMBRE_FORMATION_CHOICES,
        default='1'  # <- valeur par défaut pour éviter l'erreur MySQL
    )

    # --- Divers ---
    validite = models.DateField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)

    # --- Statut ---
    STATUT_CHOICES = [
        ('Planifiée', 'Planifiée'),
        ('En cours', 'En cours'),
        ('Complétée', 'Complétée'),
        ('Annulée', 'Annulée')
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='Planifiée'
    )

    jours_avant_expiration = models.PositiveIntegerField(default=30)

    # --- Slug ---
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                f"{self.employe.matricule}-{self.type_formation.nom}-{self.date_formation}",
                FormationChauffeur.objects
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employe} - {self.type_formation.nom}"

    class Meta:
        ordering = ["-date_formation"]
        verbose_name = "Formation Chauffeur"
        verbose_name_plural = "Formations Chauffeurs"

# ===============================
# SUIVI PASS MINE ERP-ready
# ===============================
 # Import correct du modèle Site
class SuiviPASSMine(TimeStampedModel, StatusModel, SlugModel):
    TYPE_PASS_CHOICES = [
        ('Personnel', 'Personnel'),
        ('Sous-traitant', 'Sous-traitant'),
        ('Visiteur', 'Visiteur'),
    ]
    
    STATUT_CHOICES = [
        ('Actif', 'Actif'),
        ('Expiré', 'Expiré'),
        ('Suspendu', 'Suspendu'),
        ('Annulé', 'Annulé')
    ]

    employe = models.ForeignKey(
        Employe, on_delete=models.CASCADE, related_name='suivis_pass'
    )
    numero_pass = models.CharField(max_length=50, unique=True)
    type_pass = models.CharField(max_length=20, choices=TYPE_PASS_CHOICES, default='Personnel')
    date_emission = models.DateField()
    date_expiration = models.DateField()
    responsable = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name='pass_emis'
    )
    site_emission = models.ForeignKey(
        Site, on_delete=models.SET_NULL, null=True, blank=True
    )
    jours_avant_expiration = models.PositiveIntegerField(default=30)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='Actif')
    observation = models.TextField(blank=True, null=True)

    # Relation vers les fichiers joints
    fichiers_joints = GenericRelation(FichierJoint)

    def save(self, *args, **kwargs):
        # Génération automatique du slug si inexistant
        if not self.slug:
            self.slug = slugify(f"{self.employe.nom}-{self.numero_pass}") + '-' + secrets.token_urlsafe(5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employe} - {self.numero_pass}"

    class Meta:
        ordering = ["-date_expiration"]
        verbose_name = "Suivi PASS Mine"
        verbose_name_plural = "Suivi PASS Mines"


# ===============================
# TYPES DE PERMIS   ERP-ready
class TypePermis(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    validite_par_defaut = models.PositiveIntegerField(
        default=365, help_text="Durée de validité par défaut en jours"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, TypePermis.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Type de Permis"
        verbose_name_plural = "Types de Permis"


# ===============================
# PERMIS DE TRAVAIL ERP-ready
class PermisTravail(TimeStampedModel, StatusModel, SlugModel):
    employe = models.ForeignKey(
        Employe, on_delete=models.CASCADE, related_name='permis_travail'
    )
    type_permis = models.ForeignKey(
        TypePermis, on_delete=models.CASCADE, related_name='permis'
    )
    date_emission = models.DateField()
    date_expiration = models.DateField(blank=True, null=True)
    responsable = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name='permis_emis'
    )
    site_emission = models.ForeignKey(
        Site, on_delete=models.SET_NULL, null=True, blank=True
    )
    statut = models.CharField(
        max_length=20,
        choices=[('Actif', 'Actif'), ('Expiré', 'Expiré'), ('Suspendu', 'Suspendu')],
        default='Actif'
    )
    observation = models.TextField(blank=True, null=True)

    # Relation vers les fichiers joints
    fichiers_joints = GenericRelation(FichierJoint)

    def save(self, *args, **kwargs):
        # Définir automatiquement date_expiration si non définie
        if not self.date_expiration and self.type_permis and self.date_emission:
            self.date_expiration = self.date_emission + timedelta(days=self.type_permis.validite_par_defaut)

        # Génération automatique du slug
        if not self.slug:
            self.slug = self.generate_unique_slug(
                f"{self.employe.nom}-{self.type_permis.nom}-{str(self.date_emission)}",
                PermisTravail.objects
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employe} - {self.type_permis.nom}"

    class Meta:
        ordering = ["-date_expiration"]
        verbose_name = "Permis de Travail"
        verbose_name_plural = "Permis de Travail"


# ===============================
# COMPORTEMENT ET CONDUITE ERP-ready    

# Choices pour type d'évaluation
TYPE_EVALUATION_CHOICES = [
    ('Sécurité', 'Sécurité'),
    ('Conduite', 'Conduite'),
    ('Ponctualité', 'Ponctualité'),
    ('Discipline', 'Discipline'),
    ('Autre', 'Autre'),
]

# Choices pour niveau
NIVEAU_CHOICES = [
    ('Excellent', 'Excellent'),
    ('Bon', 'Bon'),
    ('Moyen', 'Moyen'),
    ('Insuffisant', 'Insuffisant'),
]

# Choices pour statut
STATUT_CHOICES = [
    ('En attente', 'En attente'),
    ('Validée', 'Validée'),
    ('Annulée', 'Annulée'),
]

class ComportementConduite(TimeStampedModel, StatusModel, SlugModel):
    employe = models.ForeignKey(
        Employe, on_delete=models.CASCADE, related_name='comportements'
    )
    evaluateur = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations_faites'
    )
    responsable = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations_responsable'
    )
    date_evaluation = models.DateField()
    type_evaluation = models.CharField(
        max_length=50, choices=TYPE_EVALUATION_CHOICES, default='Conduite'
    )
    evaluation = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En attente')
    observation = models.TextField(blank=True, null=True)
    action_corrective = models.TextField(blank=True, null=True)
    
    # Relation vers fichiers joints
    fichiers_joints = GenericRelation(FichierJoint)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                f"{self.employe.nom}-{str(self.date_evaluation)}",
                ComportementConduite.objects
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employe} - {self.date_evaluation}"

    class Meta:
        ordering = ["-date_evaluation"]
        verbose_name = "Comportement et Conduite"
        verbose_name_plural = "Comportements et Conduites"

# ===============================
# HISTORIQUE HABILLITATION
# ===============================
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# ===============================
# HISTORIQUE HABILLITATION
# ===============================
class HistoriqueHabilitation(TimeStampedModel):
    # L'utilisateur qui fait l'action
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- au lieu de 'auth.User'
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Type d'action
    ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
        ('view', 'Consultation'),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    # Référence générique vers n'importe quel objet habilitation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Message ou description de l'action
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.action} - {self.content_object}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Historique Habilitation"
        verbose_name_plural = "Historiques Habilitations"
