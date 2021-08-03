from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django import forms
from .models import CustomUser, Recollection
from django.core.exceptions import ValidationError


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


class CustomUserEditForm(forms.Form):
    username = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    photo = forms.FileField(required=False)
    password_old = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
        required=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        not_unique_email = CustomUser.objects.filter(email=email).exists()
        not_unique_username = CustomUser.objects.filter(username=username).exists()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        password_old = cleaned_data.get("password_old")

        errors = {}
        if not_unique_email:
            errors['email'] = 'Email is already in use'
        if not_unique_username:
            errors['username'] = 'Username is already in use'
        if password1 and password2 and password1 != password2:
            errors['password1'] = 'The two password fields didn’t match.'
            errors['password2'] = 'The two password fields didn’t match.'
        if (password1 or password2) and self.user.has_usable_password():
            if not self.user.check_password(password_old):
                errors['password_old'] = 'Wrong password.'

        if errors:
            raise ValidationError(errors)
