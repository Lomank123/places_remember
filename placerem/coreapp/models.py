from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import PointField

from .managers import CustomUserManager


# TODO: add username support
class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, null=True, verbose_name="Username")
    email = models.EmailField(unique=True, verbose_name="Email address")
    photo = models.FileField(null=True, blank=True, verbose_name="Photo")

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

    # Owner of a recollection
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, verbose_name='User')

    # geojson fields
    geom = PointField(null=True)

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name_plural = 'Recollections'
        verbose_name = 'Recollection'
        ordering = ['-published']
