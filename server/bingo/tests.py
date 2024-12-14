from django.test import TestCase
from .models import Challenge, User
from django.core.exceptions import ValidationError
from datetime import date


class ChallengeTest(TestCase):
    def setUp(self):
        Challenge.objects.create(
            name="Test",
            description="This is a test challenge.",
            challenge_type="act",
            points=5,
            total_completions=10,
        )

    def test_create_challenge(self):
        challenge = Challenge.objects.get(name="Test")
        self.assertEqual(challenge.description, "This is a test challenge.")
        self.assertEqual(challenge.challenge_type, "act")
        self.assertEqual(challenge.points, 5)
        self.assertEqual(challenge.total_completions, 10)
        self.assertEqual(str(challenge), "Challenge 1: Test (Act)")

    def test_invalid_challenge_type(self):
        challenge = Challenge(
            name="Invalid Type Test",
            description="Challenge with an invalid type.",
            challenge_type="invalid_type",  # invalid value
            points=10,
        )
        with self.assertRaises(ValidationError):
            challenge.full_clean()  # validates the model instance before saving to db

    def test_default_total_completions(self):
        challenge = Challenge.objects.create(
            name="Default Completions Test",
            description="Challenge without specifying total_completions.",
            challenge_type="connect",
            points=15,
        )
        self.assertEqual(challenge.total_completions, 0)


class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Test",
            password="A generic, valid password",
            first_name="Jane",
            last_name="Doe",
            birthdate=date(1, 1, 1)
        )

    def creation(self):
        try:
            User.objects.get(username="Test")
        except User.DoesNotExist:
            self.fail("User was not properly created")

    def random_queries_fail(self):
        self.assertRaises(User.DoesNotExist, User.objects.get, username="Barry")

    def base_users_not_staff(self):
        self.assertFalse(self.user.is_staff)
