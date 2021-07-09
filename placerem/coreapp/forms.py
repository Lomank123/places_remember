from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, Recollection


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'photo')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'photo')


class RecollectionModelForm(forms.ModelForm):
    
    class Meta:
        model = Recollection
        fields = ('name', 'description', 'destination',)