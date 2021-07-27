from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView
import json

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

from .models import Recollection
from .forms import RecollectionModelForm
from .serializers import RecollectionSerializer


# Home page
@login_required
def home(request):
    recollections = Recollection.objects.filter(user=request.user)
    context = {
        'recollections' : recollections,
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