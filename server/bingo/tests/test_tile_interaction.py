from django.test import TestCase
from ..models import User, Challenge, TileInteraction, BingoGrid
from django.utils import timezone
from django.db.utils import IntegrityError


class TileInteractionTest(TestCase):
    def setUp(self):
        # Create a user, grid and challenges to be used by the tests.
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        self.grid = BingoGrid.objects.create(is_active=False)
        self.challenges = []
        for i in range(16):
            c = Challenge.objects.create(
                name=f"Challenge {i}",
                description=f"Description {i}",
                challenge_type="act",
                points=5
            )
            self.challenges.append(c)
        self.grid.challenges.add(*self.challenges)

    def test_create_tile_interaction(self):
        # Test that a TileInteraction object can be created successfully.
        interaction = TileInteraction.objects.create(
            user=self.user,
            position=2,
            grid=self.grid
        )
        self.assertFalse(interaction.completed)
        self.assertFalse(interaction.consent)
        self.assertIsNotNone(interaction.date_started)
        self.assertIsNone(interaction.date_completed)
        # For now test that image is "empty"
        self.assertFalse(interaction.image)

    def test_complete_challenge(self):
        # Test updating the 'completed' status and setting 'date_completed'.
        interaction = TileInteraction.objects.create(
            user=self.user,
            position=2,
            grid=self.grid
        )

        # simulate completion
        interaction.completed = True
        interaction.date_completed = timezone.now()
        interaction.save()

        updated_interaction = TileInteraction.objects.get(
            pk=interaction.pk)
        self.assertTrue(updated_interaction.completed)
        self.assertIsNotNone(updated_interaction.date_completed)

    def test_consent(self):
        # Test that 'consent' can be updated appropriately.
        interaction = TileInteraction.objects.create(
            user=self.user,
            position=2,
            grid=self.grid
        )
        # Initially false
        self.assertFalse(interaction.consent)
        # Update
        interaction.consent = True
        interaction.save()

        updated_interaction = TileInteraction.objects.get(
            pk=interaction.pk)
        self.assertTrue(updated_interaction.consent)

    def test_unique_user_grid_constraint(self):
        # Verifies that we cannot create two TileInteraction objects with the same (user, grid, position).
        TileInteraction.objects.create(
            user=self.user, grid=self.grid, position=2)
        with self.assertRaises(IntegrityError):
            TileInteraction.objects.create(
                user=self.user, grid=self.grid, position=2)
