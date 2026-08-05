from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from personnel.models import Employe
from parametrage.models import Societe
from documents.models import FichierJoint

# ===============================
# MIXINS PRO
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
# TYPES D'ENGINS
# ===============================
class TypeEngin(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, TypeEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Type d'engin"
        verbose_name_plural = "Types d'engins"

# ===============================
# CATEGORIES D'ENGINS
# ===============================
class CategorieEngin(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, CategorieEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Catégorie d'engin"
        verbose_name_plural = "Catégories d'engins"

# ===============================
# MARQUES ET MODELES
# ===============================
class Marque(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Marque"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, Marque.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Marque"
        verbose_name_plural = "Marques"

class Modele(TimeStampedModel, StatusModel, SlugModel):
    marque = models.ForeignKey(
        Marque,
        on_delete=models.CASCADE,
        related_name="modeles"
    )

    type_engin = models.ForeignKey(
        TypeEngin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nom = models.CharField(
        max_length=100,
        verbose_name="Modèle"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.marque.nom}-{self.nom}"
            self.slug = self.generate_unique_slug(base, Modele.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marque.nom} {self.nom}"

    class Meta:
        ordering = ["marque__nom", "nom"]
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        unique_together = ("marque", "nom", "type_engin")


# ===============================
# STATUTS DES ENGINS
# ===============================
class StatutEngin(TimeStampedModel, StatusModel, SlugModel):
    STATUTS = [
        ("DISPONIBLE", "Disponible"),
        ("MAINTENANCE", "Maintenance"),
        ("EN_SERVICE", "En service"),
        ("HORS_SERVICE", "Hors service"),
    ]

    nom = models.CharField(max_length=50, choices=STATUTS)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, StatutEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["nom"]
        verbose_name = "Statut d'engin"
        verbose_name_plural = "Statuts d'engins"

# ===============================
# SITES / DEPOTS
# ===============================
class SiteEngin(TimeStampedModel, StatusModel, SlugModel):
    nom_site = models.CharField(max_length=150)
    adresse = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom_site, SiteEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_site

    class Meta:
        ordering = ["nom_site"]
        verbose_name = "Site / Dépôt"
        verbose_name_plural = "Sites / Dépôts"

# ===============================
# ENGINS
# ===============================
class Engin(TimeStampedModel, StatusModel, SlugModel):
    immatriculation = models.CharField(max_length=50, unique=True)
    numero_chassis = models.CharField(max_length=50, blank=True, null=True)
    marque = models.ForeignKey(
        Marque,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="engins"
    )

    modele = models.ForeignKey(
        Modele,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="engins"
    )
    couleur = models.CharField(max_length=50, blank=True, null=True)
    date_mise_circulation = models.DateField(blank=True, null=True)
    date_integration_ums = models.DateField(blank=True, null=True)
    proprietaire = models.ForeignKey(Societe, on_delete=models.SET_NULL, null=True, blank=True)
    contact_proprietaire = models.CharField(max_length=50, blank=True, null=True)
    type_chassis = models.CharField(max_length=50, blank=True, null=True)
    nombre_essieux = models.PositiveIntegerField(blank=True, null=True)
    volume_benne_citerne = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_fermeture_benne = models.CharField(max_length=50, blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    site = models.ForeignKey(SiteEngin, on_delete=models.SET_NULL, null=True, blank=True)
    type_engin = models.ForeignKey(TypeEngin, on_delete=models.SET_NULL, null=True, blank=True)
    categorie = models.ForeignKey(CategorieEngin, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.ForeignKey(StatutEngin, on_delete=models.SET_NULL, null=True, blank=True)
    camion_communautaire = models.BooleanField(default=False)
    fichiers = GenericRelation(FichierJoint, related_query_name='engins')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.immatriculation, Engin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.immatriculation

    class Meta:
        ordering = ["immatriculation"]
        verbose_name = "Engin"
        verbose_name_plural = "Engins"

    def clean(self):
        super().clean()
        titres_fichiers = [f.titre.lower() for f in self.fichiers.all()]
        obligatoires = ["carte grise", "assurance", "photo engin"]
        for titre in obligatoires:
            if titre not in titres_fichiers:
                raise ValidationError(f"Le fichier obligatoire '{titre}' est manquant pour cet engin.")

        if self.type_engin:
            nom_type = self.type_engin.nom.lower()
            if "citerne" in nom_type and not self.citernes.exists():
                raise ValidationError("Un camion citerne doit avoir au moins une citerne.")
            if "benne" in nom_type and not self.remorques.exists():
                raise ValidationError("Un camion benne doit avoir au moins une remorque (benne).")

# ===============================
# REMORQUES
# ===============================
class Remorque(TimeStampedModel, StatusModel, SlugModel):
    TYPE_REMORQUE_CHOICES = [
        ("benne", "Benne"),
        ("autre", "Autre"),
    ]

    immatriculation = models.CharField(max_length=50, unique=True)
    numero_chassis = models.CharField(max_length=50, blank=True, null=True)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50, blank=True, null=True)
    volume_benne_citerne = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_remorque = models.CharField(max_length=20, choices=TYPE_REMORQUE_CHOICES, default="benne")

    tracteur = models.ForeignKey(Engin, on_delete=models.CASCADE, related_name="remorques")
    fichiers = GenericRelation(FichierJoint, related_query_name='remorques')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(f"{self.tracteur.immatriculation}-{self.immatriculation}", Remorque.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Remorque {self.immatriculation} ({self.type_remorque}) du tracteur {self.tracteur.immatriculation}"

    class Meta:
        ordering = ["immatriculation"]
        verbose_name = "Remorque"
        verbose_name_plural = "Remorques"

    def clean(self):
        super().clean()
        titres_fichiers = [f.titre.lower() for f in self.fichiers.all()]
        obligatoires = ["carte grise", "assurance", "photo engin"]
        for titre in obligatoires:
            if titre not in titres_fichiers:
                raise ValidationError(f"Le fichier obligatoire '{titre}' est manquant pour cette remorque.")
        if self.type_remorque == "benne" and not self.volume_benne_citerne:
            raise ValidationError("Le volume de la benne doit être renseigné pour une remorque de type benne.")

# ===============================
# CITERNE
# ===============================
class Citerne(TimeStampedModel, StatusModel, SlugModel):
    numero_serie = models.CharField(max_length=50, unique=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_fermeture = models.CharField(max_length=50, blank=True, null=True)
    engin = models.ForeignKey(Engin, on_delete=models.CASCADE, null=True, blank=True, related_name="citernes")
    remorque = models.ForeignKey(Remorque, on_delete=models.CASCADE, null=True, blank=True, related_name="citernes")
    fichiers = GenericRelation(FichierJoint, related_query_name='citernes')

    def save(self, *args, **kwargs):
        if not self.slug:
            cible = self.engin if self.engin else self.remorque
            if cible:
                self.slug = self.generate_unique_slug(f"{cible.immatriculation}-{self.numero_serie}", Citerne.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        cible = self.engin if self.engin else self.remorque
        return f"Citerne {self.numero_serie} de {cible}" if cible else f"Citerne {self.numero_serie}"

    class Meta:
        ordering = ["numero_serie"]
        verbose_name = "Citerne"
        verbose_name_plural = "Citernes"

    def clean(self):
        super().clean()
        titres_fichiers = [f.titre.lower() for f in self.fichiers.all()]
        if "certificat jaugeage" not in titres_fichiers:
            raise ValidationError({'fichiers': "Le certificat de jaugeage est obligatoire pour cette citerne."})

# ===============================
# INSPECTIONS ENGINS
# ===============================
ETAT_OK_NON = [
    ("ok", "OK"),
    ("non", "NON"),
]

ETAT_PF_MD = [
    ("pf", "Présent / Fonctionnel"),
    ("md", "Manquant / Défectueux"),
]
PARTIE_CHOICES = [
        ("tracteur", "Tracteur"),
        ("remorque", "Remorque"),
    ]

FUITES_CHOICES = [
    ("aucune", "Aucune"),
    ("zones_humides", "Zones humides"),
    ("gouttes", "Gouttes"),
    ("plaque_formee", "Plaque formée"),
]

DECISION_CHOICES = [
    ("apte", "Apte de circuler sans restriction"),
    ("mineures", "Présente de pannes mineures – circulation avec restrictions"),
    ("non_apte", "N’est pas apte à circuler – défaillances majeures"),
]

# ===============================
# INSPECTIONS ENGINS
# ===============================

class InspectionEngin(TimeStampedModel, SlugModel):
    
    engin = models.ForeignKey(Engin, on_delete=models.CASCADE, null=True, blank=True)
    remorque = models.ForeignKey(Remorque, on_delete=models.CASCADE, null=True, blank=True)
    
    partie = models.CharField(max_length=10, choices=PARTIE_CHOICES)
    numero_inspection = models.CharField(max_length=50)
    date_inspection = models.DateField()

    chauffeur = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name="inspections_chauffeur"
    )
    responsable = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name="inspections_responsable"
    )

    kilometrage = models.PositiveIntegerField(null=True, blank=True)
    dernier_chiffre_chassis = models.CharField(max_length=4, null=True, blank=True)
    flotte = models.CharField(max_length=50, null=True, blank=True)
    pass_mine = models.CharField(max_length=50, null=True, blank=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)

    # DOCUMENTATION (OK / NON)
    carte_grise_tracteur = models.CharField(max_length=3, choices=ETAT_OK_NON)
    carte_grise_remorque = models.CharField(max_length=3, choices=ETAT_OK_NON)

    assurance_tracteur = models.CharField(max_length=3, choices=ETAT_OK_NON)
    assurance_remorque = models.CharField(max_length=3, choices=ETAT_OK_NON)

    visite_technique_tracteur = models.CharField(max_length=3, choices=ETAT_OK_NON)
    visite_technique_remorque = models.CharField(max_length=3, choices=ETAT_OK_NON)

    permis_conduire = models.CharField(max_length=3, choices=ETAT_OK_NON)

    # FUITES
    fuite_huile_moteur = models.CharField(max_length=20, choices=FUITES_CHOICES)
    fuite_hydraulique = models.CharField(max_length=20, choices=FUITES_CHOICES)
    fuite_carburant = models.CharField(max_length=20, choices=FUITES_CHOICES)

    decision_finale = models.CharField(max_length=20, choices=DECISION_CHOICES)
    observations = models.TextField(blank=True, null=True)
    type_engin = models.ForeignKey(TypeEngin, on_delete=models.SET_NULL, null=True, blank=True)

    fichiers = GenericRelation(FichierJoint, related_query_name="inspections")

    def save(self, *args, **kwargs):
        if not self.slug:
            cible = self.engin if self.partie == "tracteur" else self.remorque
            if cible:
                self.slug = self.generate_unique_slug(f"{cible.immatriculation}-{self.numero_inspection}", InspectionEngin.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        cible = self.engin if self.partie == "tracteur" else self.remorque
        return f"Inspection {cible} - {self.date_inspection}"

    class Meta:
        ordering = ["-date_inspection"]
        verbose_name = "Inspection d'engin"
        verbose_name_plural = "Inspections d'engins"


# ===============================
# SIGNALISATION
# ===============================
class SignalisationInspection(models.Model):
    inspection = models.OneToOneField(InspectionEngin, on_delete=models.CASCADE, related_name="signalisation")

    phares_led = models.CharField(max_length=2, choices=ETAT_PF_MD)
    orientation_phares = models.CharField(max_length=2, choices=ETAT_PF_MD)
    feux_position_avant = models.CharField(max_length=2, choices=ETAT_PF_MD)
    feux_stop_arriere = models.CharField(max_length=2, choices=ETAT_PF_MD)
    feux_direction = models.CharField(max_length=2, choices=ETAT_PF_MD)
    klaxon = models.CharField(max_length=2, choices=ETAT_PF_MD)
    gyrophare = models.CharField(max_length=2, choices=ETAT_PF_MD)
    lumieres_plaques = models.CharField(max_length=2, choices=ETAT_PF_MD)


# ===============================
# EXTÉRIEUR VÉHICULE
# ===============================
class ExterieurInspection(models.Model):
    inspection = models.OneToOneField(InspectionEngin, on_delete=models.CASCADE, related_name="exterieur")

    pare_brise = models.CharField(max_length=2, choices=ETAT_PF_MD)
    retroviseurs = models.CharField(max_length=2, choices=ETAT_PF_MD)
    glaces_balais = models.CharField(max_length=2, choices=ETAT_PF_MD)
    garde_boue = models.CharField(max_length=2, choices=ETAT_PF_MD)
    ridelles_bennes = models.CharField(max_length=2, choices=ETAT_PF_MD)
    integrite_citerne = models.CharField(max_length=2, choices=ETAT_PF_MD)
    sieges_fixes = models.CharField(max_length=2, choices=ETAT_PF_MD)
    sorties_secours = models.CharField(max_length=2, choices=ETAT_PF_MD)
    volant = models.CharField(max_length=2, choices=ETAT_PF_MD)
    climatisation = models.CharField(max_length=2, choices=ETAT_PF_MD)


# ===============================
# EPI / EPC
# ===============================
class EPIInspection(models.Model):
    inspection = models.OneToOneField(InspectionEngin, on_delete=models.CASCADE, related_name="epi")
    extincteur_abc_2_9kg = models.CharField(max_length=2, choices=ETAT_PF_MD)
    extincteur_abc_6kg = models.CharField(max_length=2, choices=ETAT_PF_MD)
    trousse_pharmacie = models.CharField(max_length=2, choices=ETAT_PF_MD)
    cric_hydraulique = models.CharField(max_length=2, choices=ETAT_PF_MD)
    ceinture_securite = models.CharField(max_length=2, choices=ETAT_PF_MD)
    cle_roues = models.CharField(max_length=2, choices=ETAT_PF_MD)
    triangle_signalisation = models.CharField(max_length=2, choices=ETAT_PF_MD)
    casque_protection = models.CharField(max_length=2, choices=ETAT_PF_MD)
    lampe_torche = models.CharField(max_length=2, choices=ETAT_PF_MD)
    gilet_hv = models.CharField(max_length=2, choices=ETAT_PF_MD)
    masque_antipoussiere = models.CharField(max_length=2, choices=ETAT_PF_MD)
    ruban_balisage = models.CharField(max_length=2, choices=ETAT_PF_MD)
    gants_manutention = models.CharField(max_length=2, choices=ETAT_PF_MD)
    cales_roues = models.CharField(max_length=2, choices=ETAT_PF_MD)
    chaussures_securite = models.CharField(max_length=2, choices=ETAT_PF_MD)
    alarme_recul = models.CharField(max_length=2, choices=ETAT_PF_MD)


# ===============================
# MOTEUR
# ===============================
class MoteurInspection(models.Model):
    inspection = models.OneToOneField(InspectionEngin, on_delete=models.CASCADE, related_name="moteur")

    manometre_air = models.CharField(max_length=2, choices=ETAT_PF_MD)
    decharge_regulateur = models.CharField(max_length=2, choices=ETAT_PF_MD)
    organes_freinage = models.CharField(max_length=2, choices=ETAT_PF_MD)
    temps_remplissage_bouteilles = models.CharField(max_length=2, choices=ETAT_PF_MD)
    pression_decharge = models.CharField(max_length=2, choices=ETAT_PF_MD)
    pression_demarrage_compresseur = models.CharField(max_length=2, choices=ETAT_PF_MD)


# ===============================
# FREINAGE
# ===============================
class FreinageInspection(models.Model):
    inspection = models.OneToOneField(InspectionEngin, on_delete=models.CASCADE, related_name="freinage")

    fuite_air = models.CharField(max_length=2, choices=ETAT_PF_MD)
    controle_tuyaux_air = models.CharField(max_length=2, choices=ETAT_PF_MD)
    circuit_electrique = models.CharField(max_length=2, choices=ETAT_PF_MD)
    circuit_pneumatique_1 = models.CharField(max_length=2, choices=ETAT_PF_MD)
    circuit_pneumatique_2 = models.CharField(max_length=2, choices=ETAT_PF_MD)
    correcteur_freinage = models.CharField(max_length=2, choices=ETAT_PF_MD)
    feux_freinage = models.CharField(max_length=2, choices=ETAT_PF_MD)

# ===============================
# MÉCANISMES ET PARTIES MOBILES
# ===============================
class MecanismesInspection(models.Model):
    inspection = models.OneToOneField(
        InspectionEngin,
        on_delete=models.CASCADE,
        related_name="mecanismes"
    )

    reservoir_carburant = models.CharField(max_length=2, choices=ETAT_PF_MD)
    boucle_accrochement = models.CharField(max_length=2, choices=ETAT_PF_MD)
    support_roue_secours = models.CharField(max_length=2, choices=ETAT_PF_MD)
    systeme_frein_remorque = models.CharField(max_length=2, choices=ETAT_PF_MD)
    circuit_hydraulique = models.CharField(max_length=2, choices=ETAT_PF_MD)

# ===============================
# PARTIES MOBILES
# ===============================
class PartiesMobilesInspection(models.Model):
    inspection = models.OneToOneField(InspectionEngin, on_delete=models.CASCADE, related_name="parties_mobiles")

    reservoir_carburant = models.CharField(max_length=2, choices=ETAT_PF_MD)
    barre_accouplement = models.CharField(max_length=2, choices=ETAT_PF_MD)
    boucle_accrochage = models.CharField(max_length=2, choices=ETAT_PF_MD)
    support_roue_secours = models.CharField(max_length=2, choices=ETAT_PF_MD)
    systeme_frein_remorque = models.CharField(max_length=2, choices=ETAT_PF_MD)
    circuit_hydraulique = models.CharField(max_length=2, choices=ETAT_PF_MD)
    felures_chassis_remorque = models.CharField(max_length=2, choices=ETAT_PF_MD)
    porte_benne = models.CharField(max_length=2, choices=ETAT_PF_MD)
    fermeture_benne = models.CharField(max_length=2, choices=ETAT_PF_MD)
    bagues_direction = models.CharField(max_length=2, choices=ETAT_PF_MD)
    rotules_direction = models.CharField(max_length=2, choices=ETAT_PF_MD)
    sommier_sellette = models.CharField(max_length=2, choices=ETAT_PF_MD)
    sellette_plate = models.CharField(max_length=2, choices=ETAT_PF_MD)

    citerne = models.ForeignKey(Citerne, on_delete=models.SET_NULL, null=True, blank=True)

# ===============================
# PNEUMATIQUES
# ===============================
class PneumatiquesInspection(models.Model):
    inspection = models.OneToOneField(
        InspectionEngin,
        on_delete=models.CASCADE,
        related_name="pneumatiques"
    )

    pneus_avant = models.CharField("Pneus avant", max_length=2, choices=ETAT_PF_MD)
    pneus_arriere = models.CharField("Pneus arrière", max_length=2, choices=ETAT_PF_MD)

    pression_pneus = models.CharField("Pression des pneus", max_length=2, choices=ETAT_PF_MD)
    usure_pneus = models.CharField("Usure des pneus", max_length=2, choices=ETAT_PF_MD)

    ecrous_roues = models.CharField("Écrous de roues", max_length=2, choices=ETAT_PF_MD)
    jantes = models.CharField("Jantes", max_length=2, choices=ETAT_PF_MD)

    roue_secours = models.CharField("Roue de secours", max_length=2, choices=ETAT_PF_MD)

    def __str__(self):
        return f"Pneumatiques - {self.inspection}"


# document legaux  
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

    def __str__(self):
        return f"{self.engin.immatriculation} | {self.nom}"

    @property
    def immatriculation(self):
        return self.engin.immatriculation

    @property
    def flottes(self):
        # Retourne les flottes de l'engin sous forme de liste ou string séparé par virgule
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
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")  # <-- Nouveau champ

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
from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from django.contrib.contenttypes.fields import GenericRelation
from documents.models import FichierJoint  # Import du modèle générique de fichiers

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

    # Informations supplémentaires
    centre_controle = models.CharField(max_length=150, blank=True, null=True, verbose_name="Centre de contrôle")
    inspecteur = models.CharField(max_length=100, blank=True, null=True, verbose_name="Inspecteur")
    validite_mois = models.PositiveIntegerField(default=12, verbose_name="Validité (mois)")
    date_prochain_controle = models.DateField(blank=True, null=True, verbose_name="Prochain contrôle")
    actions_correctives = models.TextField(blank=True, null=True, verbose_name="Actions correctives")
    en_validite = models.BooleanField(default=True, verbose_name="En validité")

    # 🔗 Relation vers les fichiers joints
    documents = GenericRelation(FichierJoint, related_query_name='controle')

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
        # Calcul automatique du prochain contrôle
        if self.date_controle and self.validite_mois:
            self.date_prochain_controle = self.date_controle + relativedelta(months=self.validite_mois)

        # Mise à jour du statut en_validite
        self.en_validite = True
        if self.date_prochain_controle and self.date_prochain_controle < timezone.now().date():
            self.en_validite = False

        super().save(*args, **kwargs)

    def is_expired(self):
        """Retourne True si le contrôle est expiré"""
        if self.date_prochain_controle:
            return self.date_prochain_controle < timezone.now().date()
        return False