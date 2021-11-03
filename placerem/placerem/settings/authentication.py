import os


# Auth settings

# Sets custom user model
AUTH_USER_MODEL = 'coreapp.CustomUser'

# Login
LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/login/'

# Logout
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/login/'

# django-allauth params

# It is required by 'django.contrib.sites' app (settings.py)
SITE_ID = 1
# Should be "mandatory", "optional" or "none"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# In some cases email doesn't get retrieved so this should be set to True
ACCOUNT_EMAIL_REQUIRED = True
# This will automatically log in users after they confirm their email
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

SOCIALACCOUNT_ADAPTER = 'coreapp.authentication.SocialAccountAdapter'

# Config for django-allauth
SOCIALACCOUNT_PROVIDERS = {
    "vk": {
        "APP": {
            "client_id": int(os.environ.get('VK_OAUTH2_KEY')),
            "secret": os.environ.get('VK_OAUTH2_SECRET'),
        },
        "SCOPE": {
            "email",
        },
    },
    "github": {
        "APP": {
            "client_id": os.environ.get('GITHUB_KEY'),
            "secret": os.environ.get('GITHUB_SECRET'),
        },
        "SCOPE": {
            "user",
        },
    },
    "google": {
        "APP": {
            "client_id": os.environ.get('GOOGLE_KEY'),
            "secret": os.environ.get('GOOGLE_SECRET'),
        },
        "SCOPE": {
            "email",
        },
    },
}
