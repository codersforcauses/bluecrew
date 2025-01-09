from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from ..models import (
    User,
    Challenge,
    ChallengeInteraction,
    NullableChallengeInteraction,
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
        for i in range(8):
            c = Challenge.objects.create(
                name=f"Challenge {i}",
                description=f"Description {i}",
                challenge_type="act",
                points=5
            )
            self.challenges.append(c)
        self.grid.challenges.add(*self.challenges)
        self.nci_list = []
        for i in range(16):
            if i < 8:
                ci = ChallengeInteraction.objects.create(
                    user=self.user,
                    challenge=self.challenges[i],
                    completed=(i < 4),
                )
                nci = NullableChallengeInteraction.objects.create(
                    optional_challenge_interaction=ci)
            else:
                nci = NullableChallengeInteraction.objects.create()
            self.nci_list.append(nci)

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

        gi.challenge_interactions.add(*self.nci_list)
        gi.full_clean()
        gi.save()

        self.assertEqual(gi.challenge_interactions.count(), 16)

    def test_partial_assignment_raises_error(self):
        # If we only assign some references and then call full_clean(), we should get a ValidationError because it’s not 16.

        gi = GridInteraction.objects.create(
            user=self.user,
            grid=self.grid
        )
        gi.challenge_interactions.add(*self.nci_list[:10])

        with self.assertRaises(ValidationError) as ctx:
            gi.full_clean()

        self.assertIn("found 10", str(ctx.exception))

    def test_completion_status_correctly_determined(self):
        # Test that the get_completition_status correctly finds the completition status at each index
        gi = GridInteraction.objects.create(
            user=self.user,
            grid=self.grid
        )
        gi.challenge_interactions.add(*self.nci_list)
        self.assertTrue(all(gi.get_completition_status(i)
                        == "completed" for i in range(4)))
        self.assertTrue(all(gi.get_completition_status(i)
                        == "started" for i in range(4, 8)))
        self.assertTrue(all(gi.get_completition_status(i)
                        == "not started" for i in range(8, 16)))
