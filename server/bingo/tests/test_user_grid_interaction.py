from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from ..models import (
    User,
    Challenge,
    ChallengeInteraction,
    BingoGrid,
    GridInteraction
)


class GridInteractionTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password123'
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
        self.ci_list = []
        for ch in self.challenges:
            ci = ChallengeInteraction.objects.create(
                user=self.user,
                challenge=ch,
                completed=False,
            )
            self.ci_list.append(ci)

    def test_unique_user_grid_constraint(self):
        # Verifies that we cannot create two GridInteraction objects with the same (user, grid).
        GridInteraction.objects.create(user=self.user, grid=self.grid)
        with self.assertRaises(IntegrityError):
            GridInteraction.objects.create(user=self.user, grid=self.grid)

    def test_create_grid_interaction_strict_16(self):
        # Demonstrates we need to add exactly 16 ChallengeInteractions BEFORE calling full_clean().
        gi = GridInteraction.objects.create(
            user=self.user,
            grid=self.grid
        )

        gi.challenge_interactions.add(*self.ci_list)
        gi.full_clean()
        gi.save()

        self.assertEqual(gi.challenge_interactions.count(), 16)

    def test_partial_assignment_raises_error(self):
        # If we only assign some references and then call full_clean(), we should get a ValidationError because it’s not 16.

        gi = GridInteraction.objects.create(
            user=self.user,
            grid=self.grid
        )
        gi.challenge_interactions.add(*self.ci_list[:10])

        with self.assertRaises(ValidationError) as ctx:
            gi.full_clean()

        self.assertIn("found 10", str(ctx.exception))
