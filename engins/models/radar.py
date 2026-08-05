from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from engins.models import InspectionEngin
from personnel.models import Employe
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.exceptions import ValidationError

DUREE_VALIDITE_CHOICES = [
    (3, "3 mois"),
    (4, "4 mois"),
    (6, "6 mois"),
    (12, "1 an"),
]

class Radar(models.Model):
    inspection = models.OneToOneField(
        InspectionEngin,
        on_delete=models.CASCADE,
        related_name="radar",
        verbose_name="Inspection associée"
    )

    code_radar = models.CharField(max_length=20, unique=True, editable=False)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    date_generation = models.DateField(auto_now_add=True)
    duree_validite_mois = models.PositiveIntegerField(
        choices=DUREE_VALIDITE_CHOICES,
        default=6,
        verbose_name="Durée de validité"
    )
    date_expiration = models.DateField(blank=True, null=True)
    
    qr_code = models.ImageField(upload_to="radars/", blank=True, null=True)

    responsable_generation = models.ForeignKey(
        Employe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Responsable génération"
    )

    def clean(self):
        # Vérifie que tous les documents légaux sont valides avant création
        if self.inspection:
            engin = self.inspection.engin
            # Assurances valides ?
            assurance_ok = all(a.en_validite for a in engin.assurances.all())
            # Vignettes valides ?
            vignette_ok = all(v.date_expire >= timezone.now().date() for v in engin.vignettes.all())
            # Contrôles techniques valides ?
            controle_ok = all(c.en_validite for c in engin.controles.all())

            if not (assurance_ok and vignette_ok and controle_ok):
                raise ValidationError(
                    "Tous les documents légaux (assurances, vignettes, contrôles) doivent être valides pour générer le radar."
                )

    def save(self, *args, **kwargs):
        # Génération du code radar automatique
        if not self.code_radar:
            last = Radar.objects.order_by("id").last()
            next_id = last.id + 1 if last else 1
            self.code_radar = f"RAD-{next_id:04d}"

        # Slug sécurisé
        if not self.slug:
            self.slug = slugify(self.code_radar)

        # Calcul de la date d'expiration
        if self.date_generation and self.duree_validite_mois:
            self.date_expiration = self.date_generation + timezone.timedelta(days=30*self.duree_validite_mois)

        super().save(*args, **kwargs)

        # Génération du QR Code après sauvegarde
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(f"Radar: {self.code_radar}\nInspection: {self.inspection.slug}\nExp: {self.date_expiration}")
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            filename = f"{self.slug}.png"
            self.qr_code.save(filename, File(buffer), save=False)
            buffer.close()

            super().save(update_fields=["qr_code"])

    def __str__(self):
        return f"{self.code_radar} - {self.inspection}"

    class Meta:
        verbose_name = "Radar"
        verbose_name_plural = "Radars"
        ordering = ["-date_generation"]
