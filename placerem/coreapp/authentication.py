from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView, \
	PasswordChangeDoneView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .forms import CustomUserCreationForm


class RecLoginView(LoginView):
	template_name = "coreapp/authentication/login.html"


class RecLogoutView(LogoutView):
	next_page = '/home/'


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('/home/')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form' : form,
    }

    return render(request, 'coreapp/authentication/signup.html', context=context)


