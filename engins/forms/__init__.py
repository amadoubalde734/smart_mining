# engins/forms/__init__.py

# Formulaires engins
from .engins import (
    TypeEnginForm, CategorieEnginForm, MarqueForm, ModeleForm,
    StatutEnginForm, SiteEnginForm, EnginForm, RemorqueForm, CiterneForm
)

# Formulaires inspections
from .inspections import (
    InspectionEnginForm, SignalisationInspectionForm, ExterieurInspectionForm,
    EPIInspectionForm, MoteurInspectionForm, FreinageInspectionForm,
    PartiesMobilesInspectionForm, PneumatiquesInspectionForm, MecanismesInspectionForm
)

# Formulaires documents légaux
from .documents import (
    AssuranceEnginForm, VignetteConformiteForm,
    ControleTechniqueForm, ControleTechniqueDocumentForm,CarteGriseForm,
    CertificatJaugeageForm, CertificatJaugeageDocumentForm
)

# Formulaires événements
from .evenements import EvenementEnginForm