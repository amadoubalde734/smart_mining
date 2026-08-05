from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# SECURITY
# ==================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-key"
)


DEBUG = os.environ.get(
    "DEBUG",
    "False"
) == "True"


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
]


CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]


# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [

    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",


    # Packages
    "django_countries",
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap5",
    "rest_framework",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    "simple_history",


    # Applications métier
    "accounts",
    "backend",
    "front",
    "notifications",
    "flotte",
    "engins",
    "personnel",
    "habilitation",
    "parametrage",
    "fournisseurs",
    "documents",
    "production",
    "clients",
    "commercial",

]


if DEBUG:
    INSTALLED_APPS.append(
        "debug_toolbar"
    )


AUTH_USER_MODEL = "accounts.CustomUser"



# ==================================================
# AUTHENTIFICATION
# ==================================================

AUTHENTICATION_BACKENDS = [

    "django.contrib.auth.backends.ModelBackend",

    "allauth.account.auth_backends.AuthenticationBackend",

]



# ==================================================
# JAZZMIN
# ==================================================

JAZZMIN_SETTINGS = {

    "site_title": "Admin Mining Smart",

    "site_header": "Administration Mining Smart",

    "site_brand": "Mining Smart",

    "welcome_sign":
        "Bienvenue dans l'administration",

    "search_model":
        "accounts.customuser",

    "show_sidebar": True,

    "navigation_expanded": True,

    "hide_apps": [
        "front",
    ],

    "hide_models": [

        "auth.permission",

        "auth.group",

    ],

    "icons": {

        "accounts.customuser":
            "fas fa-user-tie",

        "auth.group":
            "fas fa-users",

        "personnel.employe":
            "fas fa-id-badge",

        "documents.fichierjoint":
            "fas fa-file",

    },

    "related_modal_active": True,

}



JAZZMIN_UI_TWEAKS = {

    "theme": "darkly",

    "navbar_small_text": False,

    "footer_small_text": True,

    "brand_color": "primary",

    "accent": "info",

}



# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.locale.LocaleMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]


if DEBUG:

    MIDDLEWARE.append(
        "debug_toolbar.middleware.DebugToolbarMiddleware"
    )



# ==================================================
# URL / WSGI
# ==================================================

ROOT_URLCONF = "smart_mining.urls"


WSGI_APPLICATION = "smart_mining.wsgi.application"



# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [

    {

        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [

            BASE_DIR / "templates"

        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.debug",

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

                "django.template.context_processors.i18n",

                "notifications.context_processors.unread_notifications",

            ],

        },

    },

]

# ==================================================
# DATABASE
# ==================================================

DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.mysql",

        "NAME": os.environ.get(
            "DB_NAME",
            "smart_mining_db"
        ),

        "USER": os.environ.get(
            "DB_USER",
            "root"
        ),

        "PASSWORD": os.environ.get(
            "DB_PASSWORD",
            ""
        ),

        "HOST": os.environ.get(
            "DB_HOST",
            "127.0.0.1"
        ),

        "PORT": os.environ.get(
            "DB_PORT",
            "3306"
        ),

        "OPTIONS": {

            "charset": "utf8mb4",

            "init_command": "SET NAMES utf8mb4",

        },

        "CONN_MAX_AGE": 600,

    }

}

# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]



# ==================================================
# CRISPY
# ==================================================

CRISPY_TEMPLATE_PACK = "bootstrap5"



# ==================================================
# LANGUAGE
# ==================================================

LANGUAGE_CODE = "fr"


TIME_ZONE = "UTC"


USE_I18N = True


USE_TZ = True



LANGUAGES = [

    ("fr", "Français"),

    ("en", "English"),

]


LOCALE_PATHS = [

    BASE_DIR / "locale",

]



# ==================================================
# STATIC / MEDIA
# ==================================================

STATIC_URL = "/static/"


STATICFILES_DIRS = [

    BASE_DIR / "static",

]


STATIC_ROOT = BASE_DIR / "staticfiles"


STORAGES = {

    "staticfiles": {

        "BACKEND":
            "whitenoise.storage.CompressedStaticFilesStorage",

    },

}

MEDIA_URL = "/media/"


MEDIA_ROOT = BASE_DIR / "media"



# ==================================================
# DEFAULT FIELD
# ==================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# ==================================================
# LOGIN
# ==================================================

LOGIN_URL = "accounts:admin_login"


LOGIN_REDIRECT_URL = "backend:dashboard"