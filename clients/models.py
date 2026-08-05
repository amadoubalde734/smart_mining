from django.db import models
from django.utils.text import slugify
from django.db.models import Max
from documents.models import FichierJoint
from django.contrib.contenttypes.fields import GenericRelation

class Client(models.Model):
    # ===============================
    # Informations de base
    # ===============================
    nom = models.CharField(max_length=150, unique=True)
    reference = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        help_text="Référence unique du client (ex: CLI0001)"
    )
    description = models.TextField(blank=True, null=True)
    actif = models.BooleanField(default=True)
    slug = models.SlugField(max_length=191, unique=True, blank=True)

    # ===============================
    # Contacts
    # ===============================
    contact_principal = models.CharField(max_length=100, blank=True, null=True)
    contact_secondaire = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telephone_fixe = models.CharField(max_length=20, blank=True, null=True)
    telephone_mobile = models.CharField(max_length=20, blank=True, null=True)

    # ===============================
    # Adresse / Géographie
    # ===============================
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    pays = models.CharField(max_length=50, blank=True, null=True)

    # ===============================
    # Informations légales / financières
    # ===============================
    numero_tva = models.CharField("N° TVA", max_length=50, blank=True, null=True)
    numero_rc = models.CharField("N° Registre Commerce", max_length=50, blank=True, null=True)
    type_client = models.CharField(
        max_length=50,
        choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise'), ('distributeur', 'Distributeur')],
        default='particulier'
    )
    limite_credit = models.DecimalField("Limite de crédit", max_digits=15, decimal_places=2, default=0)
    mode_paiement = models.CharField(
        max_length=50,
        choices=[('espece', 'Espèce'), ('virement', 'Virement'), ('cheque', 'Chèque')],
        default='espece'
    )

    # ===============================
    # Audit / Historique
    # ===============================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_derniere_commande = models.DateField(blank=True, null=True)

    # ===============================
    # Documents liés
    # ===============================
    fichiers = GenericRelation(FichierJoint, related_query_name="clients")

    class Meta:
        ordering = ["nom"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def save(self, *args, **kwargs):
        # Générer la référence si elle n'existe pas
        if not self.reference:
            last_ref = Client.objects.aggregate(max_id=Max('id'))['max_id'] or 0
            self.reference = f"CLI{str(last_ref + 1).zfill(4)}"  # CLI0001, CLI0002, etc.

        # Générer le slug si nécessaire
        if not self.slug:
            self.slug = slugify(self.nom)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.reference})"
