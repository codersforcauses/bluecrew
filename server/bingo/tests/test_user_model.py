from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from ..models import User
from django.core.exceptions import ValidationError
from datetime import date
from rest_framework.test import APIClient


class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Test",
            password="A generic, valid password",
            email="test@example.com",
            first_name="Jane",
            last_name="Doe",
            birthdate=date(1, 1, 1)
        )

    def test_creation(self):
        try:
            User.objects.get(username="Test")
        except User.DoesNotExist:
            self.fail("User was not properly created")

    def test_random_queries_fail(self):
        self.assertRaises(User.DoesNotExist,
                          User.objects.get, username="Barry")

    def test_base_users_not_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_superusers_are_staff(self):
        self.user.is_superuser = True
        self.assertTrue(self.user.is_staff)

    def test_gender_bounds(self):
        self.user.gender_identity = 7
        self.assertRaises(ValidationError, self.user.full_clean)

    def test_visibility_bounds(self):
        self.user.visibility = -1
        self.assertRaises(ValidationError, self.user.full_clean)

    def test_change_gender_identity(self):
        self.user.gender_identity = User.Gender.FEMALE
        self.user.full_clean()
        self.user.save()

    def test_username_uniqueness(self):
        self.assertRaises(
            IntegrityError,
            User.objects.create,
            username="Test",
            password="A different valid password",
            email="test@example.net"
        )

    def test_email_uniqueness(self):
        self.assertRaises(
            IntegrityError,
            User.objects.create,
            username="Assess",
            password="A string of random characters",
            email="test@example.com"
        )


class UpdatePreferencesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Test",
            password="A generic, valid password",
            email="test@example.com",
            first_name="Jane",
            last_name="Doe",
            birthdate=date(1, 1, 1),
            avatar=0,
            visibility=User.Visibility.STAFF
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def request(self, avatar=1, visibility=User.Visibility.FRIENDS, bio="words"):
        return self.client.put(
            reverse("update_preferences"),
            {"avatar": avatar, "visibility": visibility, "bio": bio}
        )

    def test_updates(self):
        self.assertEqual(self.request().status_code, 200)
        self.assertEqual(self.user.avatar, 1)
        self.assertEqual(self.user.visibility, User.Visibility.FRIENDS)
        self.assertEqual(self.user.bio, "words")

    def test_invalid(self):
        self.assertEqual(
            self.request(-1, User.Visibility.STAFF).status_code, 400)
        self.assertEqual(self.request(
            'a', User.Visibility.PUBLIC).status_code, 400)
        self.assertEqual(self.request(5, 3).status_code, 400)
        self.assertEqual(self.request(bio="!"*301).status_code, 400)

    def test_subsequent(self):
        self.assertEqual(self.request(5, 2, "").status_code, 200)
        self.assertEqual(self.request(3, 1, "other words").status_code, 200)
        self.assertEqual(self.user.visibility, 1)
        self.assertEqual(self.user.avatar, 3)
        self.assertEqual(self.user.bio, "other words")

    def test_unauthenitcated(self):
        response = APIClient().put(
            reverse("update_preferences"),
            {"avatar": 1, "visibility": User.Visibility.FRIENDS,
                "bio": "Stuff and things"}
        )
        self.assertEqual(response.status_code, 401)
