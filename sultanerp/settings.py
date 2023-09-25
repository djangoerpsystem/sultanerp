"""
Django settings for sultanerp project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

print("Welcome to SULTAN ERP SYSTEM")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-27$90p$s)ib=vh_v#r%ec_%id2&r10a%1h+ji4zajz*3i=r(nk"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# if I use DEBUG = false, the static files aren't served anymore and so i need apache or nginx to serve them i guess but i will submit the project files wihtout deployment
#DEBUG = False 

ALLOWED_HOSTS = [
    
    #ngrok for online testing my ERP App without deploying it
    #useful for evaluation, but i have to start the server on my local machine using terminal 
    # and then start ngrok with ngrok http 127.0.0.1:8000 (the same port as django server)
    # ngrok http 127.0.0.1:4040 i have access to the ngrok admin interface
    
    '64a0-2a02-3033-604-4059-294e-e30c-aeda-c9ad.ngrok-free.app',
    '127.0.0.1',
    'localhost',
    '192.168.178.*',
    '192.168.178.113',
    '192.168.178.34',
    '172.20.10.*',
    'erp.sultan-lieferservice.de',
    '*.sultan-lieferservice.de',
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #"sultanerp",
    "sultanerp.apps.SultanErpConfig",
    "chat",
    "kalender",
    "statistik",
    # "django_debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",

]

USE_L10N = True

ROOT_URLCONF = "sultanerp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # https://docs.djangoproject.com/en/4.2/ref/templates/api/#s-using-requestcontext
                'sultanerp.utilities.context_processors.dynamic_text_processor',

            ],
        },
    },
]

WSGI_APPLICATION = "sultanerp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
}

AUTH_USER_MODEL = 'sultanerp.User'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
# German
#LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

print("Timezone is: " + TIME_ZONE)

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    STATIC_DIR,
]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'sultanerp', 'cache'),
        'TIMEOUT': 3600,  # Cache data for 1 hour
    }
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# https://docs.djangoproject.com/en/4.2/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/' # dont want to have profile page yet, so defining it to here redirect to /dashboard after login
LOGOUT_REDIRECT_URL = '/accounts/login'