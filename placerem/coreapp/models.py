from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import PointField

from .managers import CustomUserManager


# TODO: add username support
class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, verbose_name="Username", null=True)
    email = models.EmailField(_('email address'), unique=True)
    photo = models.FileField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# TODO: Rebuild this model (remove distance and location fields, no need to use them in this case)
class Recollection(models.Model):
    # Default fields
    name = models.CharField(max_length=40, verbose_name='Name')
    description = models.CharField(max_length=300, verbose_name='Description')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published in')

    # Owner of a recollection
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, verbose_name='User')

    # django-leaflet fields
    geom = PointField(null=True)

    # Map fields
    #location = models.CharField(max_length=40, null=True, verbose_name='Location')
    #destination = models.CharField(max_length=100, null=True, verbose_name='Destination')
    #distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Distance')

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name_plural = 'Recollections'
        verbose_name = 'Recollection'
        ordering = ['-published']
