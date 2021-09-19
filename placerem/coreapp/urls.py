from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from coreapp.authentication import RecLoginView, RecLogoutView, CustomUserSignUpView
from coreapp.views import RecollectionDeleteView, APIRecViewSet, HomePageView, RecollectionDetailView, \
    RecollectionEditView, RecollectionCreateView, ProfileEditView, ProfilePasswordChangeView, ProfileView, \
    APICustomUserViewSet

# For testing
from django.views.generic.base import TemplateView


router = DefaultRouter()
router.register('recollections', APIRecViewSet, basename='recollections')
router.register('users', APICustomUserViewSet, basename='users')

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('add/', RecollectionCreateView.as_view(), name='add'),
    path('detail/<int:pk>/', RecollectionDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', RecollectionEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', RecollectionDeleteView.as_view(), name='delete'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile_edit'),
    # Auth paths
    path('login/', RecLoginView.as_view(), name='login'),
	path('logout/', RecLogoutView.as_view(), name='logout'),
    path('signup/', CustomUserSignUpView.as_view(), name='signup'),
    path('change_password/', ProfilePasswordChangeView.as_view(), name='change_password'),
    # Social auth
    path('auth/', include('social_django.urls', namespace='auth'), name='auth'),
    # API
    path('api/', include(router.urls)),

    # Schema
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
]