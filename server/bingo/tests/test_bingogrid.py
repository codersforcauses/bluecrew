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
