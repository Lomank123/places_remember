from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from coreapp.models import Recollection, CustomUser


class AuthenticationViewsTest(TestCase):
    
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/authentication/login.html')

    def test_logout_page(self):
        response = self.client.get(reverse('logout'))
        # Will be redirected to next page (login)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/authentication/signup.html')
        post_response = self.client.post(
            reverse('signup'),
            {
                'username': 'testusername1',
                'email': 'testemail@gmail.com', 
                'password1': 'test1234567',
                'password2': 'test1234567',
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        user = CustomUser.objects.get(username='testusername1')
        self.assertEqual(user.username, 'testusername1')
        # After creation, the user will be automatically logged in 
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
