from django.urls import path, include
from rest_framework.routers import DefaultRouter

from coreapp.views import home, blank_form, detail, add_recollection, post_rec
from coreapp.authentication import RecLoginView, RecLogoutView, signup


#router = DefaultRouter()
#router.register('recollections', APIRecollectionViewSet)

urlpatterns = [
    path('home/', home, name='home'),
    path('detail/<int:pk>', detail, name='detail'),
    path('add/', add_recollection, name='add'),
    # Auth paths
    path('login/', RecLoginView.as_view(), name='login'),
	path('logout/', RecLogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),

    path('add/api/recollections/', post_rec, name='post_rec'),
    # For testing
    #path('test/', calculate_distance_view, name='test'),
    #path('test/', blank_form, name='test'),
    #path('add/api/', include(router.urls)),
]