from pathlib import Path
import os
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# SECURITY
# =========================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-key"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
]


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Packages
    'django_countries',
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap5',
    'debug_toolbar',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'simple_history',

    # Applications métier
    'accounts',
    'backend',
    'front',
    'notifications',
    'flotte',
    'engins',
    'personnel',
    'habilitation',
    'parametrage',
    'fournisseurs',
    'documents',
    'production',
    'clients',
    'commercial',
]


AUTH_USER_MODEL = 'accounts.CustomUser'


# =========================
# JAZZMIN
# =========================

JAZZMIN_SETTINGS = {

    "site_title": "Admin Mining Smart",
    "site_header": "Administration Mining Smart",
    "site_brand": "Mining Smart",
    "welcome_sign": "Bienvenue dans l'interface d'administration",
    "copyright": "© 2025 Ta Société",

    "search_model": "accounts.customuser",

    "topmenu_links": [
        {"name": "Accueil", "url": "/", "permissions": ["auth.view_user"]},
        {"model": "accounts.customuser"},
    ],

    "icons": {
        "accounts.customuser": "fas fa-user-tie",
        "auth.group": "fas fa-users",
        "personnel.employe": "fas fa-id-badge",
        "habilitation.typeformation": "fas fa-chalkboard-teacher",
        "habilitation.formationchauffeur": "fas fa-car",
        "documents.fichierjoint": "fas fa-file",
    },

    "show_sidebar": True,
    "navigation_expanded": True,

    "hide_apps": ["front"],
    "hide_models": [
        "auth.permission",
        "auth.group"
    ],

    "related_modal_active": True,
}


JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "navbar_small_text": False,
    "footer_small_text": True,
    "brand_color": "primary",
    "accent": "info",
}


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    # Render static files
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


ROOT_URLCONF = 'smart_mining.urls'


# =========================
# TEMPLATES
# =========================

TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.debug',
                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',

                'notifications.context_processors.unread_notifications',
            ],
        },
    },
]


WSGI_APPLICATION = 'smart_mining.wsgi.application'


# =========================
# DATABASE
# =========================

# Local développement
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'smart_mining_db',

        'USER': 'root',

        'PASSWORD': '',

        'HOST': 'localhost',

        'PORT': '3306',

        'OPTIONS': {

            'charset': 'utf8mb4',

            'init_command':
            "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'; SET sql_mode='STRICT_TRANS_TABLES';",

        },

    }

}


# =========================
# PASSWORD
# =========================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


# =========================
# CRISPY
# =========================

CRISPY_TEMPLATE_PACK = "bootstrap5"


# =========================
# LANGUAGE
# =========================

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


LANGUAGES = [

    ('fr', 'Français'),

    ('en', 'English'),

]


LOCALE_PATHS = [

    BASE_DIR / 'locale',

]


# =========================
# STATIC / MEDIA
# =========================

STATIC_URL = '/static/'


STATICFILES_DIRS = [

    BASE_DIR / "static",

]


STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / "media"



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# LOGIN
# =========================

LOGIN_URL = reverse_lazy(
    'accounts:admin_login'
)

LOGIN_REDIRECT_URL = reverse_lazy(
    'backend:dashboard'
)