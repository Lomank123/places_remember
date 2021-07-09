from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium

from .models import Recollection
from .forms import RecollectionModelForm
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address


# Home page
# It should load all recollections if user logged in
# Otherwise it will show sign in or sign up buttons
def home(request):
    recollections = Recollection.objects.all()

    context = {
        'recollections' : recollections,

    }


    return TemplateResponse(request, 'coreapp/home.html', context=context)

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
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                    icon=folium.Icon(color='purple')).add_to(m)

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
                            icon=folium.Icon(color='purple')).add_to(m)
            # Destination marker
            folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                            icon=folium.Icon(color='red')).add_to(m)

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

            #print('location country: ', country)
            #print('location city: ', city)
            #print('location latitude: ', lat)
            #print('location longitude: ', lon)
            #print('###', location)
            
            # TODO: it should redirect after posting form
            #return redirect()

    m = m._repr_html_()

    context = {
        'distance' : distance,
        'form' : form,
        'map' : m,

    }

    return render(request, 'coreapp/test.html', context)