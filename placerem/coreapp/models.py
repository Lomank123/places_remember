from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators
from easy_thumbnails.fields import ThumbnailerField

from coreapp.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True, null=True, verbose_name="Username")
    email = models.EmailField(unique=True, verbose_name="Email address")
    photo = ThumbnailerField(
        null=True,
        blank=True,
        verbose_name="Photo",
        validators=[validators.FileExtensionValidator(allowed_extensions=('jpg', 'png'))],
        error_messages={'invalid_extension': 'This format does not supported'}
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Recollection(models.Model):
    # Default fields
    name = models.CharField(max_length=40, verbose_name='Name')
    description = models.CharField(max_length=300, verbose_name='Description', blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published in')
    geom = models.CharField(max_length=400, null=True, verbose_name='Coordinates')
    # Owner of a recollection
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, verbose_name='User')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Recollections'
        verbose_name = 'Recollection'
        ordering = ['-published']
