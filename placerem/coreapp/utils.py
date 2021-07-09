from django.contrib.gis.geoip2 import GeoIP2

# Help functions

# Defines all geo information using IP and returns it
def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

# Returns ip address to get user location
def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Returns center coordinates between point A and point B
def get_center_coordinates(latA, lonA, latB=None, lonB=None):
    coord = (latA, lonA)
    if latB:
        coord = [(latA + latB) / 2, (lonA + lonB) / 2]
    return coord

# Changes zoom of a map depending on distance between 2 points
def get_zoom(distance=0):
    if distance <= 100:
        return 8
    elif distance > 100 and distance <= 5000:
        return 4
    else:
        return 2 