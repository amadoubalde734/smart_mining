from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from personnel.models import Employe
from parametrage.models import Societe
from documents.models import FichierJoint
from engins.models import Engin, Remorque, Citerne, TypeEngin, TimeStampedModel, SlugModel

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

