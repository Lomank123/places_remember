from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

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
