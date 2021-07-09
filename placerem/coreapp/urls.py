from django.urls import path, include

from coreapp.views import calculate_distance_view, home


urlpatterns = [
    path('home/', home, name='home'),

    # For testing
    path('test/', calculate_distance_view, name='test'),
    
]