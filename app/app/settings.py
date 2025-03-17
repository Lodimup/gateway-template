"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

from app.app_settings import APP_SETTINGS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = APP_SETTINGS.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = APP_SETTINGS.DEBUG


ALLOWED_HOSTS = APP_SETTINGS.ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS = APP_SETTINGS.CORS_ALLOWED_ORIGINS

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "ninja",
    "corsheaders",
    # Own
    "appcore",
    "appaccount",
    "appdemo",  # remove when using this template
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 3rd party, remove if cors set in nginx
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 3rd party
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
        "DIRS": [BASE_DIR / "templates"],  # Add app directory to template dirs
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
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": APP_SETTINGS.DB_HOST,
        "NAME": APP_SETTINGS.DB_NAME,
        "USER": APP_SETTINGS.DB_USER,
        "PASSWORD": APP_SETTINGS.DB_PASS,
        "PORT": APP_SETTINGS.DB_PORT,
    },
    "OPTIONS": {
        "pool": True,
    },
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# S3
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = APP_SETTINGS.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = APP_SETTINGS.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = APP_SETTINGS.AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = APP_SETTINGS.AWS_S3_ENDPOINT_URL

# Celery Task Scheduler
CELERY_BROKER_URL = APP_SETTINGS.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = APP_SETTINGS.CELERY_RESULT_BACKEND
CELERY_TASK_TIME_LIMIT = 30 * 60

# Enables Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": APP_SETTINGS.REDIS_CACHE_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Extends the default user model
AUTH_USER_MODEL = "appaccount.User"
