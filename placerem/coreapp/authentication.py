import base64
import django
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db.models.fields import (
    BinaryField,
    DateField,
    DateTimeField,
    TimeField,
)
from django.utils import dateparse
from django.utils.encoding import force_bytes

from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from easy_thumbnails.fields import ThumbnailerField

from coreapp.forms import CustomUserCreationForm
from coreapp.models import CustomUser


class RecLoginView(LoginView):
    template_name = "coreapp/authentication/login.html"


class RecLogoutView(LogoutView):
    next_page = '/login/'


class CustomUserSignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'coreapp/authentication/signup.html'
    success_url = '/home/'

    def form_valid(self, form):
        valid = super(CustomUserSignUpView, self).form_valid(form)
        raw_password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=email, password=raw_password)
        login(self.request, user)
        return valid


# For custom adapter
SERIALIZED_DB_FIELD_PREFIX = "_db_"


# Custom adapter needed for valid deserialization (default tries to deserialize ThumbnailerField)
"""
I came up with 2 solutions:
1.  From https://github.com/pennersr/django-allauth/issues/520#issuecomment-540719064
Create adapter with overriden deserialize_instance method with additional check.
It'll pass if the field is ThumbnailerField and not throw ImproperlyConfigured exception.

2.  From the same thread as mentioned above, allauth can't work properly with custom user model so
maybe we can create separate Photo model with ThumbnailerField and ForeignKey.
Possible issues: Additional db call will be required as well as additional logic
"""


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def deserialize_instance(self, model, data):
        ret = model()
        for k, v in data.items():
            is_db_value = False
            if k.startswith(SERIALIZED_DB_FIELD_PREFIX):
                k = k[len(SERIALIZED_DB_FIELD_PREFIX):]
                is_db_value = True
            if v is not None:
                try:
                    f = model._meta.get_field(k)
                    if isinstance(f, DateTimeField):
                        v = dateparse.parse_datetime(v)
                    elif isinstance(f, TimeField):
                        v = dateparse.parse_time(v)
                    elif isinstance(f, DateField):
                        v = dateparse.parse_date(v)
                    elif isinstance(f, BinaryField):
                        v = force_bytes(base64.b64decode(force_bytes(v)))
                    # The only change is here, additional check for ThumbnailerField
                    elif is_db_value and not isinstance(f, ThumbnailerField):
                        try:
                            # This is quite an ugly hack, but will cover most
                            # use cases...
                            # The signature of `from_db_value` changed in Django 3
                            # https://docs.djangoproject.com/en/3.0/releases/3.0/#features-removed-in-3-0
                            if django.VERSION < (3, 0):
                                v = f.from_db_value(v, None, None, None)
                            else:
                                v = f.from_db_value(v, None, None)
                        except Exception:
                            raise ImproperlyConfigured(
                                "Unable to auto serialize field '{}', custom"
                                " serialization override required".format(k)
                            )
                except FieldDoesNotExist:
                    pass
            setattr(ret, k, v)
        return ret
