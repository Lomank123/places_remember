from django.test import TestCase

from coreapp.models import Recollection, CustomUser
from coreapp.serializers import RecollectionSerializer


class RecollectionSerializerTestCase(TestCase):
    
    def setUp(self) -> None:
        user = CustomUser.objects.create_user(email='testserializer@gmail.com', password='123')
        Recollection.objects.create(
            name='Rec serializer 1',
            description='Rec1',
            user=user,
        )
        Recollection.objects.create(
            name='Rec serializer 2',
            description='Rec2',
            user=user,
        )

    def test_data(self):
        rec_1 = Recollection.objects.get(name='Rec serializer 1')
        rec_2 = Recollection.objects.get(name='Rec serializer 2')

        serializer_data = RecollectionSerializer([rec_2, rec_1], many=True).data
        expected_data = [
            {
                'id': rec_2.id,
                'name': 'Rec serializer 2',
                'description': 'Rec2',
                'user': rec_2.user.pk,
                'geom': None,
            },
            {
                'id': rec_1.id,
                'name': 'Rec serializer 1',
                'description': 'Rec1',
                'user': rec_1.user.pk,
                'geom': None,
            }
        ]
        self.assertEqual(serializer_data, expected_data)
