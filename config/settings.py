"""
Django settings for the Blottr project — Vertical Slicing structure
(per CSIT327 Django Vertical Slicing + Supabase guide).
"""
from pathlib import Path
import os

from dotenv import load_dotenv 
import dj_database_url



BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = 'prelim-demo-secret-key-change-me'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Feature apps (vertical slices) — dotted path because they live
    # inside the apps/ package, not at the project root.
    'apps.login',
    'apps.register',
    'apps.home',
    'apps.user_profile',
    'apps.user_settings',
]

MIDDLEWARE = [
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
        # Project-level templates/ dir — each feature owns a subfolder
        # inside it (templates/login/, templates/register/, templates/home/).
        'DIRS': [BASE_DIR / 'templates'],
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

# --- Database ---
# Starts on SQLite; Supabase/PostgreSQL swap comes in the next step
# (section 10-14 of the guide), once vertical slicing is confirmed working.
DATABASES = {
    "default": dj_database_url.parse( 
        os.environ["DATABASE_URL"], 
        conn_max_age=600, 
        ssl_require=True, 
        )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# --- Static files ---
# STATICFILES_DIRS points at the project-level static/ dir. Each
# feature keeps its own subfolder: static/css/<feature>/, static/js/<feature>/,
# static/images/<feature>/.
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Auth flow ---
LOGIN_URL = 'login:login'
LOGIN_REDIRECT_URL = 'home:home'
LOGOUT_REDIRECT_URL = 'login:login'
