from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import login, authenticate

from coreapp.models import Recollection, CustomUser


class RecollectionViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='test@gmail.com', password='test12345')
        num = 12
        for id in range(num):
            Recollection.objects.create(
                name=f'recollection {id}',
                description=f'description {id}',
                user=user,
            )
    
    def test_home_page(self):
        # Login before accessing home page (or will get 302 status code because it'll redirect
        # to login page)
        user = CustomUser.objects.get(email='test@gmail.com')
        self.client.login(username=user.email, password='test12345')

        response = self.client.get('/home/')
        response_reverse = self.client.get(reverse('home'))
        response_paginator = self.client.get('/home/?page=2')
        # Checking accessibility
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_reverse.status_code, 200)
        self.assertEqual(response_paginator.status_code, 200)
        self.assertTemplateUsed(response, 'coreapp/home.html')
        # Checking context
        self.assertEqual(len(response.context['object_list']), 6)
        for recollection in response.context['object_list']:
            self.assertEqual(recollection.user, user)
        self.assertTrue(isinstance(response.context['object_list'][0], Recollection))
        # Paginator
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)
        self.assertEqual(response_paginator.context['page_obj'].number, 2)




