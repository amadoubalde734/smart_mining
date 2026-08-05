from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.contenttypes.fields import GenericRelation
from documents.models import FichierJoint
from engins.models import Engin, TimeStampedModel, StatusModel
    
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from engins.models import Engin, Remorque, Citerne, TimeStampedModel, StatusModel
from documents.models import FichierJoint

# Statut commun pour tous les documents
STATUTS_DOCUMENT = [
    ("VALIDE", "Valide"),
    ("EXPIRE", "Expiré"),
    ("SUSPENDU", "Suspendu"),
]

# ===============================
# ASSURANCES
# ===============================
class AssuranceEngin(TimeStampedModel, StatusModel):
    ASSURANCE_TYPES = [
        ("RCA", "Responsabilité Civile Auto"),
        ("TOUS_RISQUES", "Tous risques"),
        ("TRANSPORT", "Transport"),
        ("CHANTIER", "Assurance Chantier"),
        ("AUTRE", "Autre"),
    ]

    nom = models.CharField(max_length=150, verbose_name="Assureur")
    type_assurance = models.CharField(max_length=50, choices=ASSURANCE_TYPES, verbose_name="Type Assurance")
    date_debut = models.DateField(verbose_name="Date Début")
    date_fin = models.DateField(verbose_name="Date Validité")
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
    engin = models.ForeignKey(
        Engin,
        on_delete=models.CASCADE,
        related_name='assurances',
        verbose_name="Engin"
    )
    documents = GenericRelation(FichierJoint, related_query_name='assurance')

    # ✅ Nouveau champ
    statut = models.CharField(max_length=20, choices=STATUTS_DOCUMENT, default="VALIDE", verbose_name="Statut")

    def __str__(self):
        return f"{self.engin.immatriculation} | {self.nom}"

    @property
    def immatriculation(self):
        return self.engin.immatriculation

    @property
    def flottes(self):
        return ", ".join([f.nom for f in self.engin.flottes.all()])

    class Meta:
        ordering = ["-date_fin"]
        verbose_name = "Assurance"
        verbose_name_plural = "Assurances"
        indexes = [
            models.Index(fields=["type_assurance"]),
            models.Index(fields=["date_fin"]),
        ]

# ===============================
# VIGNETTES
# ===============================
class VignetteConformite(TimeStampedModel, StatusModel):
    TYPES_VIGNETTE = [
        ("VISITE", "Visite technique"),
        ("VIGNETTE", "Vignette fiscale"),
        ("AUTRE", "Autre"),
    ]

    engin = models.ForeignKey(Engin, on_delete=models.CASCADE, related_name='vignettes')
    date_emission = models.DateField()
    date_expire = models.DateField()
    type_vignette = models.CharField(max_length=50, choices=TYPES_VIGNETTE)
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    documents = GenericRelation(FichierJoint, related_query_name='vignette')

    # ✅ Statut
    statut = models.CharField(max_length=20, choices=STATUTS_DOCUMENT, default="VALIDE", verbose_name="Statut")

    def __str__(self):
        return f"{self.engin} - {self.type_vignette}"

    class Meta:
        ordering = ["-date_expire"]
        verbose_name = "Vignette"
        verbose_name_plural = "Vignettes"
        indexes = [
            models.Index(fields=["type_vignette"]),
            models.Index(fields=["date_expire"]),
        ]

# ===============================
# CONTRÔLES TECHNIQUES
# ===============================
class ControleTechnique(models.Model):
    RESULTATS = [
        ("CONFORME", "Conforme"),
        ("NON_CONFORME", "Non conforme"),
        ("A_REPARER", "À réparer"),
    ]

    engin = models.ForeignKey(
        Engin,
        on_delete=models.CASCADE,
        related_name='controles',
        verbose_name="Engin"
    )
    date_controle = models.DateField(verbose_name="Date du contrôle")
    resultat = models.CharField(max_length=50, choices=RESULTATS, verbose_name="Résultat")
    commentaire = models.TextField(blank=True, null=True, verbose_name="Commentaire")
    centre_controle = models.CharField(max_length=150, blank=True, null=True, verbose_name="Centre de contrôle")
    inspecteur = models.CharField(max_length=100, blank=True, null=True, verbose_name="Inspecteur")
    validite_mois = models.PositiveIntegerField(default=12, verbose_name="Validité (mois)")
    date_prochain_controle = models.DateField(blank=True, null=True, verbose_name="Prochain contrôle")
    actions_correctives = models.TextField(blank=True, null=True, verbose_name="Actions correctives")
    en_validite = models.BooleanField(default=True, verbose_name="En validité")
    documents = GenericRelation(FichierJoint, related_query_name='controle')

    # ✅ Statut
    statut = models.CharField(max_length=20, choices=STATUTS_DOCUMENT, default="VALIDE", verbose_name="Statut")

    class Meta:
        ordering = ["-date_controle"]
        verbose_name = "Contrôle Technique"
        verbose_name_plural = "Contrôles Techniques"
        indexes = [
            models.Index(fields=["resultat"]),
            models.Index(fields=["date_controle"]),
        ]

    def __str__(self):
        return f"{self.engin} - {self.resultat} ({self.date_controle})"

    def save(self, *args, **kwargs):
        if self.date_controle and self.validite_mois:
            self.date_prochain_controle = self.date_controle + relativedelta(months=self.validite_mois)
        self.en_validite = True
        if self.date_prochain_controle and self.date_prochain_controle < timezone.now().date():
            self.en_validite = False
            self.statut = "EXPIRE"
        else:
            self.statut = "VALIDE"
        super().save(*args, **kwargs)

    def is_expired(self):
        if self.date_prochain_controle:
            return self.date_prochain_controle < timezone.now().date()
        return False

# ===============================
# CERTIFICATS DE JAUGEAGE
# ===============================
class CertificatJaugeage(TimeStampedModel, StatusModel):
    engin = models.ForeignKey(
        Engin,
        on_delete=models.CASCADE,
        related_name='certificats_jaugeage',
        verbose_name="Engin"
    )
    numero_certificat = models.CharField(max_length=100, unique=True, verbose_name="Numéro du certificat")
    date_jaugeage = models.DateField(verbose_name="Date de jaugeage")
    validite_mois = models.PositiveIntegerField(default=12, verbose_name="Validité (mois)")
    date_expiration = models.DateField(blank=True, null=True, verbose_name="Date d'expiration")
    organisme = models.CharField(max_length=150, blank=True, null=True, verbose_name="Organisme certificateur")
    observations = models.TextField(blank=True, null=True)
    en_validite = models.BooleanField(default=True)
    documents = GenericRelation(FichierJoint, related_query_name='jaugeage')

    # ✅ Statut
    statut = models.CharField(max_length=20, choices=STATUTS_DOCUMENT, default="VALIDE", verbose_name="Statut")

    class Meta:
        ordering = ["-date_expiration"]
        verbose_name = "Certificat de jaugeage"
        verbose_name_plural = "Certificats de jaugeage"
        indexes = [
            models.Index(fields=["date_expiration"]),
        ]

    def __str__(self):
        return f"{self.engin.immatriculation} | {self.numero_certificat}"

    def save(self, *args, **kwargs):
        if self.date_jaugeage and self.validite_mois:
            self.date_expiration = self.date_jaugeage + relativedelta(months=self.validite_mois)
        if self.date_expiration and self.date_expiration < timezone.now().date():
            self.en_validite = False
            self.statut = "EXPIRE"
        else:
            self.en_validite = True
            self.statut = "VALIDE"
        super().save(*args, **kwargs)

    def is_expired(self):
        if self.date_expiration:
            return self.date_expiration < timezone.now().date()
        return False

STATUTS_DOCUMENT = [
    ("VALIDE", "Valide"),
    ("EXPIRE", "Expiré"),
    ("SUSPENDU", "Suspendu"),
]

class CarteGrise(TimeStampedModel, StatusModel):
    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro Carte Grise")
    date_delivrance = models.DateField(verbose_name="Date de délivrance")
    date_expiration = models.DateField(blank=True, null=True, verbose_name="Date d'expiration")
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")

    # Liens vers les propriétaires possibles
    engin = models.ForeignKey(Engin, on_delete=models.CASCADE, blank=True, null=True, related_name="cartes_grises")
    remorque = models.ForeignKey(Remorque, on_delete=models.CASCADE, blank=True, null=True, related_name="cartes_grises")
    citerne = models.ForeignKey(Citerne, on_delete=models.CASCADE, blank=True, null=True, related_name="cartes_grises")

    documents = GenericRelation(FichierJoint, related_query_name='carte_grise')
    statut = models.CharField(max_length=20, choices=STATUTS_DOCUMENT, default="VALIDE", verbose_name="Statut")

    class Meta:
        ordering = ["-date_expiration"]
        verbose_name = "Carte Grise"
        verbose_name_plural = "Cartes Grises"
        indexes = [
            models.Index(fields=["numero"]),
            models.Index(fields=["date_expiration"]),
        ]

    def __str__(self):
        cible = self.engin or self.remorque or self.citerne
        return f"{cible} | {self.numero}" if cible else f"Carte Grise {self.numero}"

    def save(self, *args, **kwargs):
        # Calcul de statut selon la date d'expiration
        if self.date_expiration and self.date_expiration < timezone.now().date():
            self.statut = "EXPIRE"
        else:
            self.statut = "VALIDE"
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        # Vérifie qu'au moins un propriétaire est renseigné
        if not (self.engin or self.remorque or self.citerne):
            raise ValidationError("La carte grise doit être attachée à un engin, une remorque ou une citerne.")

        # Vérifie que la carte grise est cohérente avec le type
        if self.engin and self.remorque:
            raise ValidationError("Une carte grise ne peut pas être attachée à la fois à un engin et à une remorque.")
        if self.citerne and self.engin:
            raise ValidationError("Une carte grise de citerne ne peut pas être attachée directement à un engin.")

        # Vérifie les fichiers obligatoires
        titres_fichiers = [f.titre.lower() for f in self.documents.all()]
        if "carte grise" not in titres_fichiers:
            raise ValidationError({'documents': "Le fichier 'Carte Grise' est obligatoire."})    