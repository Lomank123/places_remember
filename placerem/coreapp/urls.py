from django.urls import path, include
from rest_framework.routers import DefaultRouter

from coreapp.views import home, detail, add_recollection, post_rec
from coreapp.authentication import RecLoginView, RecLogoutView, signup


urlpatterns = [
    path('home/', home, name='home'),
    path('detail/<int:pk>', detail, name='detail'),
    path('add/', add_recollection, name='add'),
    # Auth paths
    path('login/', RecLoginView.as_view(), name='login'),
	path('logout/', RecLogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),

    path('add/api/recollections/', post_rec, name='post_rec'),
]