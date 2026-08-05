from django.db import models
from django.utils.text import slugify
from django.conf import settings

from clients.models import Client
from documents.models import FichierJoint
from django.contrib.contenttypes.fields import GenericRelation
from engins.models import SiteEngin
from parametrage.models import Tva
from decimal import Decimal


# ===============================
# BON DE COMMANDE
# ===============================
class BonCommande(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('annule', 'Annulé'),
    ]

    numero = models.CharField("N° Commande", max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="commandes")
    date_commande = models.DateField()
    description = models.TextField(blank=True, null=True)

    # ===============================
    # Finance / Budgétaire
    # ===============================
    code_budgetaire = models.CharField(max_length=50, blank=True, null=True)
    compte_analytique = models.CharField(max_length=50, blank=True, null=True)
    montant_ht = models.DecimalField("Montant HT", max_digits=15, decimal_places=2, null=True, blank=True)
    # TVA paramétrée
    tva = models.ForeignKey(
        Tva,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bons_commandes"
    )

    # Historisation du taux (TRÈS IMPORTANT)
    tva_taux = models.DecimalField(
        "TVA (%) appliquée",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    montant_ttc = models.DecimalField("Montant TTC", max_digits=15, decimal_places=2, null=True, blank=True)
    remise = models.DecimalField("Remise", max_digits=10, decimal_places=2, default=0)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')

    # ===============================
    # Audit
    # ===============================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, null=True, blank=True, related_name="commandes_crees"
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, null=True, blank=True, related_name="commandes_validees"
    )
    date_validation = models.DateField(null=True, blank=True)

    # ===============================
    # Documents liés
    # ===============================
    fichiers = GenericRelation(FichierJoint, related_query_name="bon_commandes")

    slug = models.SlugField(max_length=191, unique=True, blank=True)

    class Meta:
        ordering = ["-date_commande"]
        verbose_name = "Bon de Commande"
        verbose_name_plural = "Bons de Commande"

    def save(self, *args, **kwargs):
        # Slug automatique
        if not self.slug:
            self.slug = slugify(self.numero)

        # Historiser le taux TVA à la création
        if self.tva and not self.tva_taux:
            self.tva_taux = self.tva.taux

        # Calcul du montant HT depuis les lignes
        total_ht = Decimal('0.00')
        if self.pk:
            for ligne in self.lignes.all():
                if ligne.montant_ligne:
                    total_ht += ligne.montant_ligne

        self.montant_ht = total_ht

        # Calcul du TTC
        if self.tva_taux:
            self.montant_ttc = total_ht + (total_ht * self.tva_taux / Decimal('100'))
        else:
            self.montant_ttc = total_ht

        super().save(*args, **kwargs)



# ===============================
# Lignes de Bon de Commande
# ===============================
class BonCommandeLigne(models.Model):
    bon_commande = models.ForeignKey(BonCommande, on_delete=models.CASCADE, related_name="lignes")
    produit = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    quantite = models.DecimalField(max_digits=15, decimal_places=2)
    unite = models.CharField(max_length=50, blank=True, null=True)
    prix_unitaire = models.DecimalField(max_digits=15, decimal_places=2)
    montant_ligne = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.montant_ligne = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produit} | {self.quantite} {self.unite}"


# ===============================
# BON DE LIVRAISON
# ===============================
class BonLivraison(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('annule', 'Annulé'),
    ]

    numero = models.CharField("N° BL", max_length=50, unique=True)
    bon_commande = models.ForeignKey(BonCommande, on_delete=models.CASCADE, related_name="bons_livraison")
    date_livraison = models.DateField()
    site = models.ForeignKey(SiteEngin, on_delete=models.SET_NULL, null=True, blank=True, related_name="bons_livraison")
    transporteur = models.CharField(max_length=100, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')

    # ===============================
    # Audit
    # ===============================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, null=True, blank=True, related_name="bl_crees"
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, null=True, blank=True, related_name="bl_validees"
    )
    date_validation = models.DateField(null=True, blank=True)

    # ===============================
    # Documents liés
    # ===============================
    fichiers = GenericRelation(FichierJoint, related_query_name="bons_livraison")

    slug = models.SlugField(max_length=191, unique=True, blank=True)

    class Meta:
        ordering = ["-date_livraison"]
        verbose_name = "Bon de Livraison"
        verbose_name_plural = "Bons de Livraison"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.numero)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero


# ===============================
# Lignes de Bon de Livraison
# ===============================
class BonLivraisonLigne(models.Model):
    bon_livraison = models.ForeignKey(BonLivraison, on_delete=models.CASCADE, related_name="lignes")
    produit = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    quantite = models.DecimalField(max_digits=15, decimal_places=2)
    unite = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.produit} | {self.quantite} {self.unite}"
