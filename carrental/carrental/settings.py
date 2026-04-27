from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# ================= BASE DIR =================
BASE_DIR = Path(__file__).resolve().parent.parent

# ================= SECURITY =================
SECRET_KEY = 'django-insecure-9#(#!vzxg4drjnn!jmuaf(%-z%1%!blqlfjm6awrgveeco273='
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    'rest_framework',
    'accounts',
    "rental.apps.RentalConfig",

]

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('sq', _('Shqip')),
    ('en', _('English')),
    ('it', _('Italiano')),
    ('de', _('Deutsch')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]


# ================= URLS =================
ROOT_URLCONF = 'carrental.urls'


ALLOWED_HOSTS = [
    "192.168.100.3",
    "127.0.0.1",
    "localhost",
]


# ================= LANGUAGE SETTINGS =================

USE_I18N = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'superrental',   
        'USER': 'root',
        'PASSWORD': '',      
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# ================= PASSWORD =================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ================= STATIC FILES =================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

SITE_ID = 1

# ================= MEDIA =================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "orgitogjoci10@gmail.com"
EMAIL_HOST_PASSWORD = "bptfeadplccvoewk"

DEFAULT_FROM_EMAIL = "Car Rental <orgitogjoci10@gmail.com>"





DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
