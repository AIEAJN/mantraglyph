"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from . import env as env
import datetime as dt
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

current_time = str(dt.datetime.now().strftime("%H"))
current_date = str(dt.date.today())
file_name = current_time + "H_Uvicorns.log"
dir_name = str(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cr!@&0_8bfaqk8+$_&r$mmfvxe)qm8fk7c6a8j=olnf)^o3!8c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.ENV['DEBUG_MODE']

ALLOWED_HOSTS = env.ENV['ALLOWED_HOSTS']

ALLOWED_CIDR_NETS = env.ENV['ALLOWED_CIDR_NETS'] # for mobile app address authorization


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # personal imports
    'graphene_django',
    "corsheaders",
    'django_filters',
    'mantraglyph'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # personal imports
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'allow_cidr.middleware.AllowCIDRMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'

# Custom Authentication model
AUTH_USER_MODEL = 'mantraglyph.User'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Database
DATABASES = {
    'default': {
        'ENGINE': env.ENV['DATABASE_ENGINE'],
        'NAME': env.ENV['DATABASE_NAME'],
        'USER': env.ENV['DATABASE_USER'],
        'PASSWORD': env.ENV['DATABASE_PASSWORD'],
        'HOST': env.ENV['DATABASE_HOST'],
        'PORT': env.ENV['DATABASE_PORT'],
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_URL = '/var/www/mantraglyph/static/'
STATIC_ROOT = "/var/www/mantraglyph/static/"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

# Gunicorn and Uvicorn logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Adjust the log level as needed
            'class': 'logging.FileHandler',
            'filename': dir_name+file_name
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',  # Adjust the log level as needed
            'propagate': True,
        },
    },
}

GRAPHENE = {
    "SCHEMA": "mantraglyph.schema.schema",
    "RELAY_CONNECTION_MAX_LIMIT": 1000000,
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

GRAPHQL_QUERY_OPTIMIZER = {
    "ALLOW_CONNECTION_AS_DEFAULT_NESTED_TO_MANY_FIELD": True,
    "MAX_COMPLEXITY": 100,
    "DISABLE_ONLY_FIELDS_OPTIMIZATION":False
}