import os
from .settings import BASE_DIR


# Dropbox storage stuff
# 1 - use Dropbox as a media file storage
# 0 - don't use Dropbox
USE_DROPBOX = bool(int(os.environ.get('USE_DROPBOX', 0)))
if USE_DROPBOX:
    DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN')
    DROPBOX_ROOT_PATH = '/apps/places-remember'
    DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
    THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.dropbox.DropBoxStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Static
STATIC_ROOT = '/vol/web/static'
STATIC_URL = '/static/static/'

# Media
MEDIA_ROOT = '/vol/web/media'
MEDIA_URL = '/static/media/'

# Thumbnails
THUMBNAIL_MEDIA_ROOT = '/vol/web/media/thumbnails'
THUMBNAIL_MEDIA_URL = '/static/media/thumbnails/'
THUМВNAIL_DEFAULT_OPТIONS = {'quality': 90, 'subsampling': 1, }
THUMBNAIL_ALIASES = {
    # Preset for user photo
    'placerem.CustomUser.photo': {
        'default_user_photo': {
            'size': (150, 200),
            'crop': 'scale',
        },
        'small_user_photo': {
            'size': (50, 50),
            'crop': 'scale',
        },
    },
    # Presets for the whole project
    '': {
        'default': {
            'size': (180, 240),
            'crop': 'scale',
        },
        'big': {
            'size': (480, 640),
            'crop': '10,10',
        },
        'small': {
            'size': (30, 30),
            'crop': 'scale',
        },
    },
}
