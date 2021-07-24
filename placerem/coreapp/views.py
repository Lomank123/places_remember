from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
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
def detail(request, pk):
    recollection = Recollection.objects.get(pk=pk)
    context = {
        'recollection' : recollection,
    }
    return TemplateResponse(request, 'coreapp/rec_detail.html', context=context)

# Recollection create page
@login_required
def add_recollection(request):
    if request.method == 'GET':
        context = {
            'collections' : Recollection.objects.filter(user=request.user),
        }
        return TemplateResponse(request, 'coreapp/add_recollection.html', context=context)

# Handles post request to create recollection 
@login_required
@api_view(['POST', 'GET'])
def post_rec(request):
    #if request.method == 'GET':
    #    recs = Recollection.objects.all()
    #    serializer = RecollectionSerializer(recs, many=True)
    #    return Response(serializer.data)
    if request.method == 'POST':
        new_data = request.data
        serializer = RecollectionSerializer(data=new_data)
        print(request.data)

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
