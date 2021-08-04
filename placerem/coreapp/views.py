from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import json

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

from .models import Recollection, CustomUser
from .forms import RecollectionModelForm, CustomUserEditForm
from .serializers import RecollectionSerializer


# Home page
@login_required
def home(request):
    recollections = Recollection.objects.filter(user=request.user)

    # Paginator
    objects_per_page = 6
    paginator = Paginator(recollections, objects_per_page)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    
    context = {
        'recollections' : page.object_list,
        'page' : page,
    }
    return TemplateResponse(request, 'coreapp/home.html', context=context)

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
    if request.method == 'GET':
        recollection = Recollection.objects.get(pk=pk)
        context = {
            'recollection' : recollection,
            'method' : 'PUT',
        }
        return TemplateResponse(request, 'coreapp/rec_add_edit.html', context=context)

# Recollection create page
@login_required
def rec_add(request):
    if request.method == 'GET':
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
@login_required
@api_view(['POST', 'PUT'])
def rec_api(request):
    new_data = request.data
    serializer = RecollectionSerializer(data=new_data)

    if serializer.is_valid():
        if "lng" in new_data:
            point = {
                "type" : "Point",
                "coordinates" : [new_data["lng"], new_data["lat"]],
            }
        else:
            point = None
        serializer.validated_data["geom"] = point
        serializer.validated_data["user"] = request.user

        if request.method == 'POST':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'PUT':
            instance = Recollection.objects.get(pk=new_data["id"])
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecDeleteView(DeleteView):
    model = Recollection
    success_url = '/home/'
    template_name = 'coreapp/confirmation/recollection_confirm_delete.html'