from django.test import TestCase
from ..models import Challenge
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
        # Build expected string around challenge rather than hard coded id
        expected_str = f"Challenge {challenge.id}: {
            challenge.name} ({challenge.challenge_type.capitalize()})"
        self.assertEqual(str(challenge), expected_str)

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
