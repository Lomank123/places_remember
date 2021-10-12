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

# Social auth

# VK
SOCIAL_AUTH_VK_OAUTH2_KEY = int(os.environ.get('SOCIAL_AUTH_VK_OAUTH2_KEY'))
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']   # additionally receives user's email address
# GitHub
SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']  # additionally receives user's email address

# If you're using Postgres database this should be enabled
SOCIAL_AUTH_JSONFIELD_ENABLED = True
# If you want to use the full email address as username, set this to True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
