"""
Django settings for play project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import dotenv


def get_env(key, default=None, allow_default=True):
    if key not in os.environ:
        if allow_default:
            print("using default value for %s=%s" % (key, default))
            return default
        raise NotImplementedError("Environment variable is unset: '%s'" % key)
    return os.environ[key]



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get environment variable ENV from the system
# default to production if it doesn't exist
ENV = get_env('ENV', 'production', True)

def is_local_env():
    return ENV == 'local'

def is_production_env():
    return ENV == 'production'

if is_local_env():
    # Read environment values from the .env file
    dot_env_path = os.path.join(BASE_DIR + "/.env")
    dotenv.read_dotenv(dot_env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env("BATTLESNAKEIO_SECRET", "thisshouldbeset", True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if is_production_env() else True

ALLOWED_HOSTS = []

if is_production_env():    
    ALLOWED_HOSTS = [ get_env("BATTLESNAKEIO_DOMAIN", None, False) ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.authentication',
    'apps.tournament',
    'apps.snake',
    'apps.game',
    'social_django',
    'widget_tweaks',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            (os.path.join(BASE_DIR, 'templates'))
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if is_production_env():
    '''
    Only enable the PG config if we're running in production
    '''
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': get_env("BATTLESNAKEIO_POSTGRES_DB", "battlesnakeio_play", True),
            'USER': get_env("BATTLESNAKEIO_POSTGRES_USER", None, False),
            'PASSWORD': get_env("BATTLESNAKEIO_POSTGRES_PASSWORD", None, False),
            'HOST': get_env("BATTLESNAKEIO_POSTGRES_HOST", None, False),
            'PORT': get_env("BATTLESNAKEIO_POSTGRES_PORT", None, False),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GITHUB_KEY = get_env('BATTLESNAKEIO_GITHUB_CLIENT_ID')
SOCIAL_AUTH_GITHUB_SECRET = get_env('BATTLESNAKEIO_GITHUB_CLIENT_SECRET')
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
AUTH_USER_MODEL = 'authentication.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


ENGINE_URL = get_env('ENGINE_URL', 'http://localhost:3005')
BOARD_URL = get_env('BOARD_URL', 'http://localhost:3000')

# Silencing system checks that are unneeded.
# https://docs.djangoproject.com/en/2.1/ref/checks/

SILENCED_SYSTEM_CHECKS = ['fields.W342']
