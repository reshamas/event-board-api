"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from django.core.management.utils import get_random_secret_key
from pathlib import Path
import dj_database_url
import os
import sys
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = os.path.join(BASE_DIR, '.env')

LOCALHOST_CLIENT_ORIGIN = 'http://localhost:3000'

# SECURITY WARNING: don't run with debug turned on in production!
if os.path.exists(ENV_PATH):
    env = environ.Env()
    environ.Env.read_env(ENV_PATH)
    DEBUG = env('DEBUG') == 'True'
    DEVELOPMENT_MODE = env('DEVELOPMENT_MODE') == 'True'
    AUTH_COOKIE_DOMAIN = 'localhost'
else:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'False') == 'True'
    AUTH_COOKIE_DOMAIN = os.environ.get('PROD_COOKIE_DOMAIN', '')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
DYNAMIC_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

if DEVELOPMENT_MODE:
    STATIC_HOSTS = ['localhost']
else:
    STATIC_HOSTS = [os.getenv('CLIENT_HOST')]

ALLOWED_HOSTS = DYNAMIC_HOSTS + STATIC_HOSTS

if DEVELOPMENT_MODE:
    MAGIC_LINK_DOMAIN = LOCALHOST_CLIENT_ORIGIN
else:
    MAGIC_LINK_DOMAIN = os.getenv('CLIENT_ORIGIN')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drfpasswordless',
    'events',
    'authentication',
    'storages',
    'contact_emails',
    'weekly_digest',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_DATABASE'),
                'USER': os.environ.get('DB_USERNAME'),
                'PASSWORD': os.environ.get('DB_PASSWORD'),
                'HOST': os.environ.get('DB_HOST'),
                'PORT': os.environ.get('DB_PORT'),
            }
        }
    else:
        DATABASES = {
            "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
        }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
     ],
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.middleware.HttpOnlyTokenAuthentication'
     ],
     'TEST_REQUEST_DEFAULT_FORMAT': 'json',
     'DEFAULT_FILTER_BACKENDS': [
       'django_filters.rest_framework.DjangoFilterBackend',
     ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

if DEVELOPMENT_MODE:
    CORS_ALLOWED_ORIGINS = [LOCALHOST_CLIENT_ORIGIN]
else:
    CORS_ALLOWED_ORIGINS = [os.getenv('CLIENT_ORIGIN')]

CORS_ALLOW_HEADERS = [
  'accept-encoding',
  'authorization',
  'content-disposition',
  'content-type', 'accept',
  'origin',
]

SESSION_COOKIE_PATH = '/;HttpOnly'
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
    'accept',
    'set-cookie'
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

auth_template_name = 'authentication/auth.html'

PASSWORDLESS_AUTH = {
    'PASSWORDLESS_EMAIL_SUBJECT': 'Data Event Board: Sign In',
    'PASSWORDLESS_AUTH_TYPES': ['EMAIL'],
    'PASSWORDLESS_EMAIL_NOREPLY_ADDRESS': 'noreply@specollective.org',
    'PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME': 'authentication/auth.html',
    'PASSWORDLESS_CONTEXT_PROCESSORS': [
        'authentication.context_processors.passwordless_email_processor',
    ],
    'PASSWORDLESS_USER_MARK_EMAIL_VERIFIED': True,
    'PASSWORDLESS_USER_EMAIL_VERIFIED_FIELD_NAME': 'email_verified',
}

if DEVELOPMENT_MODE:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST_USER = 'example@example.com'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


AUTH_USER_MODEL = 'authentication.CustomUser'

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

AWS_DEFAULT_ACL = 'public-read'
AWS_S3_REGION_NAME = 'nyc3'
AWS_STORAGE_BUCKET_NAME = 'event-board-storage'
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
