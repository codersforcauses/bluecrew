from django.test import TestCase
from ..models import Challenge, BingoGrid
from django.core.exceptions import ValidationError


class BingoGridTest(TestCase):
    def setUp(self):
        self.challenges = []
        for i in range(16):
            c = Challenge.objects.create(
                name=f"Challenge {i}",
                description="A sample challenge",
                challenge_type="act",
                points=5
            )
            self.challenges.append(c)

    def test_exactly_16_challenges(self):
        # Verify a BingoGrid with exactly 16 challenges passes validation, but 15 or 17 fails.
        grid = BingoGrid.objects.create(is_active=False)

        grid.challenges.add(*self.challenges)
        grid.full_clean()
        grid.save()
        # 15 challenge scenario
        grid_15 = BingoGrid.objects.create(is_active=False)
        grid_15.challenges.add(*self.challenges[:15])
        with self.assertRaises(ValidationError):
            grid_15.full_clean()

        # 17 challenge scenario
        extra_challenge = Challenge.objects.create(
            name="Extra Challenge",
            description="Extra sample challenge",
            challenge_type="act",
            points=10
        )
        grid_17 = BingoGrid.objects.create(is_active=False)
        grid_17.challenges.add(*self.challenges)
        grid_17.challenges.add(extra_challenge)
        with self.assertRaises(ValidationError):
            grid_17.full_clean()

    def test_preserve_challenge_order(self):
        # With SortedManyToManyField, the order we add them is retained.
        grid = BingoGrid.objects.create(is_active=False)
        for c in reversed(self.challenges):
            grid.challenges.add(c)
        sorted_list = list(grid.challenges.all())
        self.assertEqual(sorted_list[0], self.challenges[15])
        self.assertEqual(sorted_list[-1], self.challenges[0])
        grid.full_clean()

    def test_single_active_grid(self):
        # Ensure that only one BingoGrid can be active at once.
        grid1 = BingoGrid.objects.create(is_active=True)
        grid1.challenges.add(*self.challenges)
        grid1.full_clean()
        grid1.save()

        # Second grid tries to be active
        grid2 = BingoGrid.objects.create(is_active=True)
        grid2.challenges.add(*self.challenges)
        with self.assertRaises(ValidationError):
            grid2.full_clean()

        # Make grid2 inactive, now it should be valid
        grid2.is_active = False
        grid2.full_clean()
        grid2.save()
