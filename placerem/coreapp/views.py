from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.views import PasswordChangeView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from coreapp.models import Recollection, CustomUser
from coreapp.forms import CustomUserEditForm
from coreapp.serializers import RecollectionSerializer, CustomUserSerializer


# Home page
class HomePageView(LoginRequiredMixin, ListView):
    model = Recollection
    template_name = 'coreapp/home.html'
    paginate_by = 6

    # Without overriding this method other users will be able to get your data
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


# Recollection create page
class RecollectionCreateView(LoginRequiredMixin, CreateView):
    model = Recollection
    fields = ['name', 'description']
    template_name = 'coreapp/rec_add_edit.html'
    success_url = '/home/'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_info"] = {
            'user_id': self.request.user.pk,
        }
        return context


# Detailed information about certain recollection
class RecollectionDetailView(LoginRequiredMixin, DetailView):
    model = Recollection
    template_name = 'coreapp/rec_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_info"] = {
            'user_id': self.request.user.pk,
            'rec_id': self.get_object().pk
        }
        return context


# Recollection delete page
class RecollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Recollection
    success_url = '/home/'
    template_name = 'coreapp/confirmation/recollection_confirm_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


# Recollection edit page (uses put method to update recollections)
class RecollectionEditView(LoginRequiredMixin, UpdateView):
    model = Recollection
    fields = ['name', 'description']
    template_name = 'coreapp/rec_add_edit.html'
    success_url = '/home/'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_info"] = {
            'user_id': self.request.user.pk,
            'rec_id': self.get_object().pk
        }
        return context


# Handles all requests when creating or editing recollection
class APIRecViewSet(ModelViewSet):
    serializer_class = RecollectionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Recollection.objects.filter(user=self.request.user)
        return queryset


class APICustomUserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = CustomUser.objects.filter(pk=self.request.user.pk)
        return queryset


# Profile page
class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'coreapp/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recollections"] = Recollection.objects.filter(user=self.request.user).count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(pk=self.request.user.pk)
        return queryset


# Profile edit page
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'coreapp/profile_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.cleaned_data["delete_photo"]:
            self.object.photo = ''
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset().filter(pk=self.request.user.pk)
        return queryset


# Password change page
class ProfilePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'coreapp/authentication/change_password.html'
    success_url = '/home/'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})
