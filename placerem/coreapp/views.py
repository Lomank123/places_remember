from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import DeleteView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Recollection, CustomUser
from .forms import CustomUserEditForm
from .serializers import RecollectionSerializer


# Home page
class HomePageView(LoginRequiredMixin, ListView):
    model = Recollection
    template_name = 'coreapp/home.html'
    paginate_by = 6

    def get_queryset(self):
        # To get recollections of a current user
        queryset = super(HomePageView, self).get_queryset()
        return queryset.filter(user=self.request.user)
    

# Detailed information about certain recollection
@login_required
def rec_detail(request, pk):
    recollection = Recollection.objects.get(pk=pk)
    context = {
        'recollection' : recollection,
    }
    return TemplateResponse(request, 'coreapp/rec_detail.html', context=context)

@login_required
def rec_edit(request, pk):
    recollection = Recollection.objects.get(pk=pk)
    context = {
        'recollection' : recollection,
        'method' : 'PUT',
    }
    return TemplateResponse(request, 'coreapp/rec_add_edit.html', context=context)

# Recollection create page
@login_required
def rec_add(request):
    context = {
        'method' : 'POST',
    }
    return TemplateResponse(request, 'coreapp/rec_add_edit.html', context=context)

@login_required
def profile(request):
    # Deleting photo
    if request.method == 'POST':
        user = request.user
        user.photo = None
        user.save()
        return redirect('/profile/')
    context = {
        'recollections' : Recollection.objects.filter(user=request.user).count,
    }
    return TemplateResponse(request, 'coreapp/profile.html', context=context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.user, request.POST, request.FILES)

        if form.is_valid():
            instance = get_object_or_404(CustomUser, id=request.user.pk)
            # If it's possible make it in a more elegant way
            if form.cleaned_data['username']:
                instance.username = form.cleaned_data['username']
            if form.cleaned_data['email']:
                instance.email = form.cleaned_data['email']
            if form.cleaned_data['photo']:
                instance.photo = form.cleaned_data['photo']
            if form.cleaned_data['password1'] and form.cleaned_data['password2']:
                instance.set_password(form.cleaned_data['password1'])
            instance.save()
            return redirect('/profile/')
    else:
        form = CustomUserEditForm(request.user)
    
    context = {
        'form' : form,
        'has_password' : request.user.has_usable_password()
    }
    return TemplateResponse(request, 'coreapp/profile_edit.html', context=context)


# Handles post and put requests when creating or editing recollection
class APIRecViewSet(ModelViewSet):
    queryset = Recollection.objects.all()
    serializer_class = RecollectionSerializer
    permission_classes = (IsAuthenticated, )


class RecDeleteView(DeleteView):
    model = Recollection
    success_url = '/home/'
    template_name = 'coreapp/confirmation/recollection_confirm_delete.html'