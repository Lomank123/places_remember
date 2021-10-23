import os


# Auth settings

# Sets custom user model
AUTH_USER_MODEL = 'coreapp.CustomUser'

# Login
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'

# Logout
LOGOUT_URL = '/logout/'
LOGIN_URL = '/login/'

# django-allauth params

# It is required by 'django.contrib.sites' app (settings.py)
SITE_ID = 1
# Verification should be "none" otherwise there'll be an error with api callback
ACCOUNT_EMAIL_VERIFICATION = "none"
# In some cases email doesn't get retrieved so this should be set to True
ACCOUNT_EMAIL_REQUIRED = True

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
