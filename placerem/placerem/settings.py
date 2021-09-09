import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

# Auth
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'

LOGOUT_URL = '/logout/'
LOGIN_URL = '/login/'

# Social auth
SOCIAL_AUTH_VK_OAUTH2_KEY = int(os.environ.get('SOCIAL_AUTH_VK_OAUTH2_KEY'))
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')
#SOCIAL_AUTH_FACEBOOK_KEY = int(os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY'))
#SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')
# When db is postgres
SOCIAL_AUTH_JSONFIELD_ENABLED = True
# If you want to use the full email address as the username, define this setting.
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
# If you want to receive an email address of user
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Sets custom user model
AUTH_USER_MODEL = 'coreapp.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coreapp',
    'crispy_forms',
    'djgeojson',
    'rest_framework',
    'corsheaders',
    'social_django',
    'easy_thumbnails',
    'django_cleanup',
    'storages',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'placerem.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'placerem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST', 'db'),
        'NAME': os.environ.get('DB_NAME', 'devdb'),
        'USER': os.environ.get('DB_USER', 'devuser'),
        'PASSWORD': os.environ.get('DB_PASS', 'devpassword'),
    }
}

# Heroku db setup
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Storage stuff
USE_DROPBOX = os.environ.get('USE_DROPBOX') == 'TRUE'
if USE_DROPBOX:
    DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN')
    DROPBOX_ROOT_PATH = '/apps/places-remember'
    DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
    THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.dropbox.DropBoxStorage'

# Static
STATIC_ROOT = '/vol/web/static'
STATIC_URL = '/static/static/'

# Media
MEDIA_ROOT = '/vol/web/media'
MEDIA_URL = '/static/media/'

# Thumbnails
THUMBNAIL_MEDIA_ROOT = '/vol/web/media/thumbnails'
THUMBNAIL_MEDIA_URL = '/static/media/thumbnails/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'coreapp/static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Thumbnails
THUМВNAIL_DEFAULT_OPТIONS = {'quality': 90, 'subsampling': 1,}
THUMBNAIL_ALIASES = {
    # Preset for user photo
    'placerem.CustomUser.photo' : {
        'default_user_photo' : {
            'size' : (150, 200),
            'crop' : 'scale',
        },
        'small_user_photo' : {
            'size' : (50, 50),
            'crop' : 'scale',
        },
    },
    # Presets for the whole project
    '' : {
        'default' : {
            'size' : (180, 240),
            'crop' : 'scale',
        },
        'big' : {
            'size' : (480, 640),
            'crop' : '10,10',
        },
        'small' : {
            'size' : (30, 30),
            'crop' : 'scale',
        },
    },
}