"""
Django settings for the project2 application.

This file contains settings and configurations for the Django project, including
security settings, database configurations, installed apps, middleware, and more.

For detailed information on settings:
    - General settings: https://docs.djangoproject.com/en/5.1/topics/settings/
    - Full list of settings: https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ
import dj_database_url

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = environ.Env()
environ.Env.read_env()

# Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = env('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = env('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = env('SPOTIPY_REDIRECT_URI')

# Security settings
SECRET_KEY = env('SECRET_KEY')  # Secret key for the project
DEBUG = False  # Debug mode should be off in production
ALLOWED_HOSTS = ['*']  # Allow all hosts in development; restrict in production

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # End session when browser closes

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend.apps.FrontendConfig',  # Frontend app
    'spotify.apps.SpotifyConfig',  # Spotify app
    'wraps.apps.WrapsConfig',  # Wraps app
    'storages',  # S3 storage
]

# Middleware configuration
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

# Template settings
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

# WSGI application
WSGI_APPLICATION = 'project2.wsgi.application'

# Database configuration using environment variables
DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = 'https://spotify-wrapped.s3.amazonaws.com/static/'

# AWS S3 settings for file storage
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'spotify-wrapped'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False

STORAGES = {
    # Media files
    "default": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
    # Static files
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'frontend:login'
LOGIN_REDIRECT_URL = 'frontend:index'

# Developer comments for API keys and configurations (Example placeholders)
# Akshaya
# SPOTIPY_CLIENT_ID = 'your_client_id'
# SPOTIPY_CLIENT_SECRET = 'your_client_secret'
# SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify/callback'

# Arnav
# SPOTIPY_CLIENT_ID = 'your_client_id'
# SPOTIPY_CLIENT_SECRET = 'your_client_secret'
# SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify/redirect/'
