from django.test import TestCase
from django.urls import reverse

from coreapp.models import Recollection


class RecollectionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num = 12

        for id in range(num):
            Recollection.objects.create(
                name=f'recollection {id}',
                description=f'description {id}',
            )
        
    def test_recollection_access(self):
        i = 11
        for obj in Recollection.objects.all():
            self.assertEqual(obj.name, "recollection {0}".format(i))
            i -= 1