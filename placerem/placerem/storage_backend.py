from settings import STATIC_LOCATION, PUBLIC_MEDIA_LOCATION, PUBLIC_MEDIA_THUMBNAILS_LOCATION
from storages.backends.s3boto3 import S3Boto3Storage


# Static files storage
class StaticStorage(S3Boto3Storage):
    location = STATIC_LOCATION
    default_acl = 'public-read'


# Media files storage
class PublicMediaStorage(S3Boto3Storage):
    location = PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    file_overwrite = False


# Thumbnails storage (inside media storage)
class ThumbnailsMediaStorage(S3Boto3Storage):
    location = '{PUBLIC_MEDIA_LOCATION}/{PUBLIC_MEDIA_THUMBNAILS_LOCATION}'
    default_acl = 'public-read'
    file_overwrite = False