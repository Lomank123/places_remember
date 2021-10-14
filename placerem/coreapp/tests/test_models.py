import json
from django.test import TestCase
from django.contrib.auth import get_user_model

from coreapp.models import Recollection, CustomUser


# User model tests
class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        # str() method
        self.assertEqual(str(user), user.email)

        # Labels
        label_name_username = user._meta.get_field('username').verbose_name
        self.assertEqual(label_name_username, 'Username')
        max_length_username = user._meta.get_field('username').max_length
        self.assertEqual(max_length_username, 40)
        label_name_email = user._meta.get_field('email').verbose_name
        self.assertEqual(label_name_email, 'Email address')
        label_name_photo = user._meta.get_field('photo').verbose_name
        self.assertEqual(label_name_photo, 'Photo')
        # Fields
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class RecollectionModelTest(TestCase):

    # Initializing data
    def setUp(self) -> None:

        point = {
            "coordinates": [100.00, 20.00],
        }
        user = CustomUser.objects.create_user(email='testmodel@gmail.com')
        Recollection.objects.create(
            name='Rec model test',
            description='Rec description',
            user=user,
            geom=json.dumps(point),
        )

    def test_recollection_str(self):
        recollection = Recollection.objects.get(name='Rec model test')
        self.assertEqual(str(recollection), recollection.name)

    # Name field
    def test_name_field(self):
        recollection = Recollection.objects.get(name='Rec model test')
        self.assertEqual(recollection.name, 'Rec model test')

    def test_name_label(self):
        recollection = Recollection.objects.get(name='Rec model test')
        label_name = recollection._meta.get_field('name').verbose_name
        self.assertEqual(label_name, 'Name')

    def test_name_max_length(self):
        recollection = Recollection.objects.get(name='Rec model test')
        max_length = recollection._meta.get_field('name').max_length
        self.assertEqual(max_length, 40)

    # Description field
    def test_description_field(self):
        recollection = Recollection.objects.get(name='Rec model test')
        self.assertEqual(recollection.description, 'Rec description')

    def test_description_label(self):
        recollection = Recollection.objects.get(name='Rec model test')
        label_name = recollection._meta.get_field('description').verbose_name
        self.assertEqual(label_name, 'Description')

    def test_description_max_length(self):
        recollection = Recollection.objects.get(name='Rec model test')
        max_length = recollection._meta.get_field('description').max_length
        self.assertEqual(max_length, 300)

    # Published in field
    def test_published_date_label(self):
        recollection = Recollection.objects.get(name='Rec model test')
        label_name = recollection._meta.get_field('published').verbose_name
        self.assertEqual(label_name, 'Published in')

    # User field
    def test_user_label(self):
        recollection = Recollection.objects.get(name='Rec model test')
        label_name = recollection._meta.get_field('user').verbose_name
        self.assertEqual(label_name, 'User')

    def test_user_foreign_key(self):
        recollection = Recollection.objects.get(name='Rec model test')
        self.assertEqual(recollection.user.email, 'testmodel@gmail.com')

    # geom field
    def test_geom_field(self):
        recollection = Recollection.objects.get(name='Rec model test')
        point = {
            "coordinates": [100.00, 20.00],
        }
        self.assertEqual(json.loads(recollection.geom), point)
