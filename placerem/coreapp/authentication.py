from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

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


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)
