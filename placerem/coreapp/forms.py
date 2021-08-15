from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.core.exceptions import ValidationError

from coreapp.models import CustomUser, Recollection


class CustomUserCreationForm(UserCreationForm):


    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'photo')


class CustomUserChangeForm(UserChangeForm):


    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'photo')


class RecollectionModelForm(forms.ModelForm):
    

    class Meta:
        model = Recollection
        fields = ('name', 'description', 'geom')


class CustomUserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    photo = forms.FileField(required=False, widget=forms.FileInput)
    delete_photo = forms.BooleanField(required=False, initial=False)


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'photo']
