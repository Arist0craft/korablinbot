"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from pathlib import Path

import environ

from utils import setup_logger

logger = setup_logger(__name__)

# Set default values to environmental variables
env = environ.Env(
    DEBUG=(bool, True),
    MC_PORT=(int, 25565),
    MC_CONNECTION_TRIES=(int, 10),
    MC_CONNECTION_WAIT=(int, 30),
    REDIS_URL=(str, "redis://redis:6379"),
    SECRET_KEY=(str, "django-insecure-p-!4&^*$s^bp1rr80emp5b*ixt)4hp$(kwha=x09^q%(+tw#(s"),
    TGBOT_DEBUG=(bool, True),
    USE_CELERY=(bool, True),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent


if (env_file_path := Path(BASE_DIR / ".env")).exists():
    environ.Env.read_env(env_file_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = env("DEBUG")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tgbot.apps.TgBotConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Set tgbot settings
TGBOT_SETTINGS = {
    "DEBUG": env("TGBOT_DEBUG"),
    "HOST": env("TGBOT_HOST"),
    "TOKEN": env("TGBOT_TOKEN"),
    "MC_PORT": env("MC_PORT"),
    "MC_HOST": env("MC_HOST"),
    "MC_CONNECTION_TRIES": env("MC_CONNECTION_TRIES"),
    "MC_CONNECTION_WAIT": env("MC_CONNECTION_WAIT"),
}

# Celery configuration
USE_CELERY: bool = env("USE_CELERY")
REDIS_URL: str = env("REDIS_URL")
BROKER_URL: str = REDIS_URL
CELERY_BROKER_URL: str = REDIS_URL
CELERY_RESULT_BACKEND: str = REDIS_URL
CELERY_ACCEPT_CONTENT: list = ['application/json']
CELERY_TASK_SERIALIZER: str = 'json'
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_TIMEZONE: str = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE: str = 'default'

OCI_SETTING = {
    "user": env("OCI_USER"),
    "fingerprint": env("OCI_FINGERPRINT"),
    "tenancy": env("OCI_TENANCY"),
    "region": env("OCI_REGION"),
    "key_content": env.str("OCI_KEY_CONTENT", multiline=True),
    "instance_id": env("OCI_INSTANCE_ID"),
}
