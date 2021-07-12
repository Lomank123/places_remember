from django.urls import path, include

from coreapp.views import calculate_distance_view, home, blank_form, detail
from coreapp.authentication import RecLoginView, RecLogoutView, signup


urlpatterns = [
    path('home/', home, name='home'),
    path('detail/<int:pk>', detail, name='detail'),
    # Auth paths
    path('login/', RecLoginView.as_view(), name='login'),
	path('logout/', RecLogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),

    # For testing
    path('test/', calculate_distance_view, name='test'),
    #path('test/', blank_form, name='test'),

]