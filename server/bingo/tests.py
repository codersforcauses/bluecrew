from django.test import TestCase, Client
from .models import Challenge
from django.core.exceptions import ValidationError


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


class RegisterUserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_user(self):
        response = self.client.post(
            '/register/', {'username': 'test_user', 'email': 'test@gmail.com',
                           'first_name': 'larry', 'last_name': 'bird', 'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 201)

    def test_register_user_error(self):
        response = self.client.post(
            '/register/', {'username': 'forgotten_fields', 'email': 'test@gmail.com',
                           'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 400)
