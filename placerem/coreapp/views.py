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

# For detailed information about certain recollection
def detail(request, pk):
    recollection = Recollection.objects.get(pk=pk)
    context = {
        'recollection' : recollection,
    }
    return TemplateResponse(request, 'coreapp/rec_detail.html', context=context)

@login_required
def add_recollection(request):
    if request.method == 'GET':
        context = {
            'collections' : Recollection.objects.all(),
        }


        return TemplateResponse(request, 'coreapp/add_recollection.html', context=context)


@api_view(['POST', 'GET'])
def post_rec(request):
    if request.method == 'GET':
        recs = Recollection.objects.all()
        serializer = RecollectionSerializer(recs, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        new_data = request.data
        new_rec = Recollection()
        new_rec.name = new_data["name"]
        new_rec.description = new_data["description"]
        new_rec.user = request.user

        new_coords = []
        #for i in new_data["geom"]

        point = {
            "type" : "Point",
            "coordinates" : new_data["geom"],
        }
        new_rec.geom = point

        new_data["geom"] = point
        new_rec.save()
        return Response(new_data, status=status.HTTP_201_CREATED)

        #serializer = RecollectionSerializer(data=new_data)
        #print(request.data)
        #if serializer.is_valid():
        #    serializer.user = request.user
        #    
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #print(serializer.errors)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class APIRecollectionViewSet(ModelViewSet):
#	queryset = Recollection.objects.all()
#	serializer_class = RecollectionSerializer


# For testing (for local purposes, without map)
def blank_form(request):
    form = RecollectionModelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.user = request.user
            instance.save()
    
    context = {
        'form' : form,
    }

    return TemplateResponse(request, 'coreapp/test_blank.html', context)

"""
# For testing
def calculate_distance_view(request):
    form = RecollectionModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='coreapp')

    # Google ip address
    ip = '72.14.207.99'
    ip_ = get_ip_address(request)
    print(ip_)
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)

    # Location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    distance = 0.00

    # TODO: Maybe delete this later
    # Initial Folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon),
                     zoom_start=2)

    # Location marker
    new_marker = folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                    icon=folium.Icon(color='purple'), draggable=True)
    new_marker.add_to(m)
    
    print(m._children.values())
    print(list(m._children.values())[1].location)

    if request.method == 'POST':
        # For testing
        if form.is_valid():
            instance = form.save(commit=False)
            destination_ = form.cleaned_data.get('destination')
            destination = geolocator.geocode(destination_)
            print(destination)
            
            # Destination coordinates
            d_lat = destination.latitude
            d_lon = destination.longitude
            pointB = (d_lat, d_lon)

            # Distance calculation
            distance = round(geodesic(pointA, pointB).km, 2)

            # Folium map modification
            m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
                             zoom_start=get_zoom(distance))
            # Location marker
            folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                            icon=folium.Icon(color='purple'), draggable=True).add_to(m)
            # Destination marker
            folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                            icon=folium.Icon(color='red'), draggable=True).add_to(m)

            # Draw the line between location and destination
            line = folium.PolyLine(locations=[pointA, pointB], weight=2, color='blue')
            m.add_child(line)

            instance.location = location
            instance.distance = distance
            instance.destination = destination
            if request.user.is_authenticated:
                instance.user = request.user
            instance.save()
            #context.update({'distance' : instance.distance})
            print(new_marker.location)
            #print('location country: ', country)
            #print('location city: ', city)
            #print('location latitude: ', lat)
            #print('location longitude: ', lon)
            #print('###', location)
            
            #return redirect('/home/')

    m = m._repr_html_()

    context = {
        'distance' : distance,
        'form' : form,
        'map' : m,
    }

    return TemplateResponse(request, 'coreapp/test.html', context)
"""
