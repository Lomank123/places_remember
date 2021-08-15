from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.views import PasswordChangeView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from coreapp.models import Recollection, CustomUser
from coreapp.forms import CustomUserEditForm
from coreapp.serializers import RecollectionSerializer


# Home page
class HomePageView(LoginRequiredMixin,ListView):
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.cleaned_data["delete_photo"]:
            self.object.photo = ''
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class ProfilePasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    template_name = 'coreapp/authentication/change_password.html'
    success_url = '/home/'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


# Handles post and put requests when creating or editing recollection
class APIRecViewSet(ModelViewSet):
    queryset = Recollection.objects.all()
    serializer_class = RecollectionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
    
