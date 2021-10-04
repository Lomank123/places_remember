from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from coreapp.models import Recollection, CustomUser


class RecollectionViewsTest(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create_user(email='test@gmail.com', password='test12345')
        # Login before accessing home page (or will get 302 status code because it'll redirect to login page)
        self.client.login(username=user.email, password='test12345')
        num = 12
        for id in range(num):
            Recollection.objects.create(
                name=f'recollection {id}',
                description=f'description {id}',
                user=user,
            )
        # Second user (for access tests)
        user2 = CustomUser.objects.create_user(email='test2@gmail.com', password='test12345')
        Recollection.objects.create(name='Other recollection 1', user=user2)

    def test_home_page_view(self):
        user = CustomUser.objects.get(email='test@gmail.com')
        response = self.client.get(reverse('home'))
        response_paginator = self.client.get('/home/?page=2')
        # Checking accessibility
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_paginator.status_code, status.HTTP_200_OK)
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

    # Recollection views
    def test_rec_create_view(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/rec_add_edit.html')
        post_response = self.client.post(
            reverse('add'),
            {'name': 'test create 1', 'description': 'test create 1'}
        )
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        rec = Recollection.objects.get(name='test create 1')
        self.assertTrue(isinstance(rec, Recollection))
        self.assertEqual(rec.name, 'test create 1')

    def test_rec_detail_view(self):
        rec = Recollection.objects.get(name='recollection 0')
        response = self.client.get(reverse('detail', kwargs={'pk': rec.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/rec_detail.html')
        self.assertContains(response, rec.name, status_code=status.HTTP_200_OK)
        self.assertContains(response, rec.description, status_code=status.HTTP_200_OK)
        # Wrong request (user is logged in)
        rec_2 = Recollection.objects.get(name='Other recollection 1')
        response = self.client.get(reverse('detail', kwargs={'pk': rec_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # user2 is logged in
        self.client.login(username='test2@gmail.com', password='test12345')
        response = self.client.get(reverse('detail', kwargs={'pk': rec_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Again wrong request
        response = self.client.get(reverse('detail', kwargs={'pk': rec.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rec_delete_view(self):
        rec = Recollection.objects.get(name='recollection 0')
        response = self.client.get(reverse('delete', kwargs={'pk': rec.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/confirmation/recollection_confirm_delete.html')
        # Wrong request (user is logged in)
        rec_2 = Recollection.objects.get(name='Other recollection 1')
        response = self.client.get(reverse('delete', kwargs={'pk': rec_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # user2 is logged in
        self.client.login(username='test2@gmail.com', password='test12345')
        response = self.client.get(reverse('delete', kwargs={'pk': rec_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Again wrong request
        response = self.client.get(reverse('delete', kwargs={'pk': rec.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rec_edit_view(self):
        rec = Recollection.objects.get(name='recollection 0')
        response = self.client.get(reverse('edit', kwargs={'pk': rec.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/rec_add_edit.html')
        post_response = self.client.post(
            reverse('edit', kwargs={'pk': rec.pk}),
            {'name': 'test edit 1', 'description': 'test edit 1'}
        )
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        rec.refresh_from_db()
        self.assertTrue(isinstance(rec, Recollection))
        self.assertEqual(rec.name, 'test edit 1')
        # Wrong request (user is logged in)
        rec_2 = Recollection.objects.get(name='Other recollection 1')
        response = self.client.get(reverse('edit', kwargs={'pk': rec_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # user2 is logged in
        self.client.login(username='test2@gmail.com', password='test12345')
        response = self.client.get(reverse('edit', kwargs={'pk': rec_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Again wrong request
        response = self.client.get(reverse('edit', kwargs={'pk': rec.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Profile views
    def test_profile_view(self):
        user = CustomUser.objects.get(email='test@gmail.com')
        user2 = CustomUser.objects.get(email='test2@gmail.com')
        response = self.client.get(reverse('profile', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/profile.html')
        self.assertContains(response, user.email, status_code=status.HTTP_200_OK)
        self.assertContains(response, user.username, status_code=status.HTTP_200_OK)
        # Wrong request (user is logged in)
        response = self.client.get(reverse('profile', kwargs={'pk': user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # user2 is logged in
        self.client.login(username='test2@gmail.com', password='test12345')
        response = self.client.get(reverse('profile', kwargs={'pk': user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Again wrong request
        response = self.client.get(reverse('profile', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_edit_view(self):
        user = CustomUser.objects.get(email='test@gmail.com')
        user2 = CustomUser.objects.get(email='test2@gmail.com')
        response = self.client.get(reverse('profile_edit', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/profile_edit.html')
        post_response = self.client.post(
            reverse('profile_edit', kwargs={'pk': user.pk}),
            {'username': 'test user 1'},
        )
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        user.refresh_from_db()
        self.assertEqual(user.username, 'test user 1')
        # Wrong request (user is logged in)
        response = self.client.get(reverse('profile_edit', kwargs={'pk': user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # user2 is logged in
        self.client.login(username='test2@gmail.com', password='test12345')
        response = self.client.get(reverse('profile_edit', kwargs={'pk': user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Again wrong request
        response = self.client.get(reverse('profile_edit', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_password_change_view(self):
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'coreapp/authentication/change_password.html')
