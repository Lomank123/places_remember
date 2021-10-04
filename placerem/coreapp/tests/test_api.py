import json
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from coreapp.models import Recollection, CustomUser
from coreapp.serializers import RecollectionSerializer


class RecollectionAPITestCase(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create_user(email='testapi@gmail.com', password='123')
        user2 = CustomUser.objects.create_user(email='testapi2@gmail.com', password='123')
        # post and put methods are testing using user2
        self.client.login(username='testapi2@gmail.com', password='123')

        Recollection.objects.create(
            name='Rec api 1',
            description='Rec1',
            user=user,
        )
        Recollection.objects.create(
            name='Rec api 2',
            description='Rec2',
            user=user,
        )
        Recollection.objects.create(
            name='Rec api 3',
            description='Rec3',
            user=user2,
        )
        # data for user2
        self.valid_rec = {
            'name': 'Valid rec 1',
            'description': 'Valid description 1',
            'user': user2.pk,
            'geom': 'null'
        }
        self.invalid_rec = {
            'name': '',
            'description': 'Valid description 1',
            'user': user2.pk,
            'geom': 'null'
        }

    def test_post_valid(self):
        response = self.client.post(
            reverse('recollections-list'),
            data=json.dumps(self.valid_rec),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid(self):
        response = self.client.post(
            reverse('recollections-list'),
            data=json.dumps(self.invalid_rec),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid(self):
        rec = Recollection.objects.get(name='Rec api 3')
        rec.name = 'New rec api 3'
        serializer_data = RecollectionSerializer(rec).data
        """
        We're calling put method here because ModelViewSet creates
        2 routes: first for POST and GET methods and the second for PUT, PATCH and DELETE methods.
        The second route comes with pk argument.
        """
        response = self.client.put(
            reverse('recollections-list') + str(rec.pk) + '/',
            data=json.dumps(serializer_data),
            content_type='application/json'
        )
        self.assertEqual(Recollection.objects.get(id=rec.pk).name, 'New rec api 3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_invalid(self):
        rec = Recollection.objects.get(name='Rec api 3')
        rec.name = ''
        serializer_data = RecollectionSerializer(rec).data

        response = self.client.put(
            reverse('recollections-list') + str(rec.pk) + '/',
            data=json.dumps(serializer_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get(self):
        self.client.login(username='testapi@gmail.com', password='123')
        response = self.client.get(reverse('recollections-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rec_1 = Recollection.objects.get(name='Rec api 1')
        rec_2 = Recollection.objects.get(name='Rec api 2')
        serializer_data = RecollectionSerializer([rec_2, rec_1], many=True).data
        self.assertEqual(serializer_data, response.data)
