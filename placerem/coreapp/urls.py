from django.urls import path, include
from rest_framework.routers import DefaultRouter

from coreapp.views import home, rec_detail, rec_add, rec_edit, rec_api, profile, \
    RecDeleteView, profile_edit
from coreapp.authentication import RecLoginView, RecLogoutView, signup


urlpatterns = [
    path('home/', home, name='home'),
    path('add/', rec_add, name='add'),
    path('detail/<int:pk>/', rec_detail, name='detail'),
    path('edit/<int:pk>/', rec_edit, name='edit'),
    path('delete/<int:pk>/', RecDeleteView.as_view(), name='delete'),
    path('profile/', profile, name='profile'),
    path('profile/edit', profile_edit, name='profile_edit'),
    # Auth paths
    path('login/', RecLoginView.as_view(), name='login'),
	path('logout/', RecLogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    # Social auth
    path('auth/', include('social_django.urls', namespace='auth'), name='auth'),
    # API
    path('api/recollections/', rec_api, name='rec_api'),
]