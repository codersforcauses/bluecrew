"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_URLS = os.environ.get("FRONTEND_URLS").split()
FRONTEND_URL = FRONTEND_URLS[0]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("API_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("APP_ENV") == "DEVELOPMENT"

ALLOWED_HOSTS = (
    os.environ.get("API_ALLOWED_HOSTS").split()
    if os.environ.get("API_ALLOWED_HOSTS")
    else []
)

# SimpleJWT configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # this needs to match the id field for the user model specified in models.py
    "USER_ID_FIELD": "user_id",

    "SIGNING_KEY": SECRET_KEY,
    'UPDATE_LAST_LOGIN': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Change this to point to custom user model
AUTH_USER_MODEL = "bingo.User"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    "bingo",
    "sortedm2m",
    "django_q"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ALLOWED_ORIGINS = FRONTEND_URLS

CSRF_TRUSTED_ORIGINS = (
    os.environ.get("CSRF_TRUSTED_ORIGINS").split()
    if os.environ.get("CSRF_TRUSTED_ORIGINS")
    else []
)

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["bingo/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME") or "postgres",
        "USER": os.environ.get("POSTGRES_USER") or "postgres",
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD") or "password",
        "HOST": os.environ.get("POSTGRES_HOST") or "host.docker.internal",
        "PORT": os.environ.get("POSTGRES_PORT") or 5432,
    }
}

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 1,
    'timeout': 90,
    'retry': 120,
    'orm': 'default'
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Email address to send account management emails
ACCOUNTS_EMAIL = os.environ.get("ACCOUNTS_EMAIL")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend"

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Log to file in production
# Source: https://mattsegal.dev/file-logging-django.html
if not DEBUG and os.environ.get("GITHUB_ACTION") is None:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {"level": "INFO", "handlers": ["file"]},
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": "/var/log/django/django.log",
                "formatter": "app",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": True
            },
        },
        "formatters": {
            "app": {
                "format": (
                    u"%(asctime)s [%(levelname)-8s] "
                    "(%(module)s.%(funcName)s) %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
    }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))  # <- '/' directory

STATIC_URL = "/static/"

# STATIC_ROOT is where the static files get copied to when "collectstatic" is run.
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static_files")

# This is where to _find_ static files when 'collectstatic' is run.
# These files are then copied to the STATIC_ROOT location.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)

MEDIA_DIR = "challenge_images/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR)

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Points for completing bingo line and grid
BINGO_COMPLETE = 100
GRID_COMPLETE = 500
