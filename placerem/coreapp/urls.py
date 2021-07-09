from django.urls import path, include

from coreapp.views import calculate_distance_view, home, blank_form, detail


urlpatterns = [
    path('home/', home, name='home'),

    # For testing
    path('test/', calculate_distance_view, name='test'),
    #path('test/', blank_form, name='test'),
    path('detail/<int:pk>', detail, name='detail'),

]