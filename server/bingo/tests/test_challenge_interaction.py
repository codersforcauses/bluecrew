from django.test import TestCase
from ..models import User, Challenge, ChallengeInteraction
from django.utils import timezone


class ChallengeInteractionTest(TestCase):
    def setUp(self):
        # Create a user and a challenge to be used by the tests.
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        self.challenge = Challenge.objects.create(
            name="Testing Challenge",
            description="Challenge for testing interactions",
            challenge_type="act",
            points=5,
        )

    def test_create_challenge_interaction(self):
        # Test that a ChallengeInteraction can be created successfully.
        interaction = ChallengeInteraction.objects.create(
            user=self.user,
            challenge=self.challenge
        )
        self.assertEqual(interaction.completed, 0)
        self.assertFalse(interaction.consent)
        self.assertIsNone(interaction.date_started)
        self.assertIsNone(interaction.date_completed)
        # For now test that image is "empty"
        self.assertFalse(interaction.image)

    def test_start_challenge(self):
        # Test updating the 'completed' status to 'started' and setting 'date_started'.
        interaction = ChallengeInteraction.objects.create(
            user=self.user,
            challenge=self.challenge
        )

        # simulate completion
        interaction.completed = 1
        interaction.date_started = timezone.now()
        interaction.save()

        updated_interaction = ChallengeInteraction.objects.get(
            pk=interaction.pk)
        self.assertEqual(updated_interaction.completed, 1)
        self.assertIsNotNone(updated_interaction.date_started)

    def test_complete_challenge(self):
        # Test updating the 'completed' status to 'completed' and setting 'date_completed'.
        interaction = ChallengeInteraction.objects.create(
            user=self.user,
            challenge=self.challenge
        )

        # simulate completion
        interaction.completed = 2
        interaction.date_completed = timezone.now()
        interaction.save()

        updated_interaction = ChallengeInteraction.objects.get(
            pk=interaction.pk)
        self.assertEqual(updated_interaction.completed, 2)
        self.assertIsNotNone(updated_interaction.date_completed)

    def test_consent(self):
        # Test that 'consent' can be updated appropriately.
        interaction = ChallengeInteraction.objects.create(
            user=self.user,
            challenge=self.challenge
        )
        # Initially false
        self.assertFalse(interaction.consent)
        # Update
        interaction.consent = True
        interaction.save()

        updated_interaction = ChallengeInteraction.objects.get(
            pk=interaction.pk)
        self.assertTrue(updated_interaction.consent)
