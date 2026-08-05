# engins/models/__init__.py
from .engin import Engin, Remorque, Citerne, TimeStampedModel, SlugModel, StatusModel,TypeEngin,CategorieEngin,StatutEngin
from .evenements import EvenementEngin, TypeEvenement, StatutCamionEvenement, StatutRadarEvenement
from .inspections import (
    InspectionEngin, SignalisationInspection, ExterieurInspection, EPIInspection,
    MoteurInspection, FreinageInspection, MecanismesInspection, PartiesMobilesInspection,
    PneumatiquesInspection,ETAT_OK_NON,ETAT_PF_MD, FUITES_CHOICES, DECISION_CHOICES, PARTIE_CHOICES
    


)
from .radar import Radar
from .documents_legaux import AssuranceEngin, VignetteConformite, ControleTechnique,CertificatJaugeage
from .engin import SiteEngin, Marque,Modele