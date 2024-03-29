"""
Django settings for fit project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import socket
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'fitapp.apps.FitappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'django_static_fontawesome',
    'django_q',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'fit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'tags_extras': 'fitapp.tags_extras',
            }
        },
    },
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


WSGI_APPLICATION = 'fit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')

MEDIA_URL = '/uploads/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


HOSTNAME = socket.gethostname()

if HOSTNAME == 'MacBook-Air-de-Oscar.local':
    URL_BASE = 'http://127.0.0.1:9001'
    REDIRECT_URI = 'http://127.0.0.1:9001/oauth/login/'
else:
    URL_BASE = 'https://mimifit.herokuapp.com'
    REDIRECT_URI = 'https://mimifit.herokuapp.com/oauth/login/'
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


GOOGLEFIT_CONFIG = {
    'CLIENT_ID': env('OAUTH_CLIENT_ID'),
    'APP_SECRET_KEY': env('OAUTH_APP_SECRET_KEY'),
    'OAUTH_API_KEY': env('OAUTH_API_KEY'),
    'REDIRECT_URI': REDIRECT_URI,
    'access_token_uri': 'https://accounts.google.com/o/oauth2/token',
    'durationMillis': 86400000,
    'url_aggregate': "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate",
    'url_session': "https://www.googleapis.com/fitness/v1/users/me/sessions?startTime=%(startTime)s&endTime=%(endTime)s",
    #'url_dataSets': "https://fitness.googleapis.com/fitness/v1/users/me/dataSources?key=%(key)s",
    #'url_dataSources': "https://fitness.googleapis.com/fitness/v1/users/me/dataSources/%(dataStreamId)s/dataPointChanges?key=%(key)s",
    'dataTypeDistanceName': "com.google.distance.delta",
    'dataTypeStepsName':  "com.google.step_count.delta",
    'dataTypeCaloriesName':  "com.google.calories.expended",
    'dataTypeActiveName':  "com.google.active_minutes",
    'dataTypeHeartName': "com.google.heart_minutes",
    'dataTypeFatName': "com.google.body.fat.percentage",
    'dataTypeActivitySegmentName': "com.google.activity.segment",
    'dataTypeWattsName': "com.google.power.sample",
    'dataTypeSleepName': "com.google.sleep.segment",
    'OAUTH_SCOPES': 'https://www.googleapis.com/auth/fitness.sleep.read https://www.googleapis.com/auth/fitness.heart_rate.read https://www.googleapis.com/auth/fitness.reproductive_health.read https://www.googleapis.com/auth/fitness.body_temperature.read https://www.googleapis.com/auth/fitness.oxygen_saturation.read https://www.googleapis.com/auth/fitness.blood_glucose.read https://www.googleapis.com/auth/fitness.blood_pressure.read https://www.googleapis.com/auth/fitness.nutrition.read https://www.googleapis.com/auth/fitness.body.read https://www.googleapis.com/auth/fitness.location.read https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/userinfo.profile',
    'timedelta_session': 0,
}



X_FRAME_OPTIONS = 'SAMEORIGIN'



# Q_CLUSTER CONF
Q_CLUSTER = {
    'name': 'fitapp',
    'workers': 1,
    'recycle': 500,
    'orm': 'default',
    'timeout': 900,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'retry': 1200,
    'max_attempts': 3,
    'label': 'Django Q',
}
# Q_CLUSTER CONF

# SENDGRID CONF #
#SENDGRID_API_KEY = env('SENDGRID_API_KEY')

#EMAIL_HOST = 'smtp.sendgrid.net'
#EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
#EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
# SENDGRID CONF #
