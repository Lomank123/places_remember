from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, CreateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import PasswordChangeView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Recollection, CustomUser
from .forms import CustomUserEditForm
from .serializers import RecollectionSerializer


# Home page
class HomePageView(ListView, LoginRequiredMixin):
    model = Recollection
    template_name = 'coreapp/home.html'
    paginate_by = 6

    def get_queryset(self):
        # To get recollections of a current user
        queryset = super(HomePageView, self).get_queryset()
        return queryset.filter(user=self.request.user)


# Detailed information about certain recollection
class RecollectionDetailView(DetailView, LoginRequiredMixin):
    model = Recollection
    template_name = 'coreapp/rec_detail.html'


# Recollection edit page
class RecollectionEditView(UpdateView, LoginRequiredMixin):
    model = Recollection
    fields = ['name', 'description']
    template_name = 'coreapp/rec_add_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["method"] = 'PUT'
        return context


# Recollection create page
class RecollectionCreateView(CreateView, LoginRequiredMixin):
    model = Recollection
    fields = ['name', 'description']
    template_name = 'coreapp/rec_add_edit.html'


# Recollection delete page
class RecollectionDeleteView(DeleteView, LoginRequiredMixin):
    model = Recollection
    success_url = '/home/'
    template_name = 'coreapp/confirmation/recollection_confirm_delete.html'


# Profile page
class ProfileView(DetailView, LoginRequiredMixin):
    model = CustomUser
    template_name = 'coreapp/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recollections"] = Recollection.objects.filter(user=self.request.user).count()
        return context
    

class ProfileEditView(UpdateView, LoginRequiredMixin):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'coreapp/profile_edit.html'
    success_url = '/profile/'


class ProfilePasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    template_name = 'coreapp/authentication/change_password.html'
    success_url = '/home/'


# Handles post and put requests when creating or editing recollection
class APIRecViewSet(ModelViewSet):
    queryset = Recollection.objects.all()
    serializer_class = RecollectionSerializer
    permission_classes = (IsAuthenticated, )
