"""
Django settings for project2 project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lzv9$dqw@a(@qn28hv&#xxs(&1yyb@evp(ejgjp95xfq_0&a@+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend.apps.FrontendConfig',
    'spotify.apps.SpotifyConfig',
    'wraps.apps.WrapsConfig',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project2.urls'

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

WSGI_APPLICATION = 'project2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# Render Database Stuff
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    # Add any other languages you want
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'https://spotify-wrapped.s3.amazonaws.com/static/'
# STATICFILES_DIRS = [BASE_DIR / "static"]

#AWS Configuration
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY =  env('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'spotify-wrapped'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False


STORAGES = {
    #Media files
    "default" : {
        "BACKEND" : "storages.backends.s3boto3.S3StaticStorage",
    },
    #CSS and JS file management
    "staticfiles": {
        "BACKEND" : "storages.backends.s3boto3.S3StaticStorage",
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Akshaya
# SPOTIPY_CLIENT_ID = 'cd6b9651745b4329962c82234b0064c3'
# SPOTIPY_CLIENT_SECRET = '1feec18903eb4a8eba79f1b5d16b2d56'
# SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify/callback'

# Arnav
# SPOTIPY_CLIENT_ID = 'cd6b9651745b4329962c82234b0064c3'
# SPOTIPY_CLIENT_SECRET = '1feec18903eb4a8eba79f1b5d16b2d56'
# SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify/redirect/'

# LOGIN_URL = '/accounts/login/'

LOGIN_URL = 'frontend:login'
LOGIN_REDIRECT_URL = 'frontend:index'


