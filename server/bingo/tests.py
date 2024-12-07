from django.test import TestCase
from .models import Challenge


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
