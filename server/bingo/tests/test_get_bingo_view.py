from django.test import TestCase
from rest_framework.test import APIClient
from ..models import BingoGrid, Challenge, TileInteraction, User
from django.urls import reverse


class GetBingoGridTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.active_grid = BingoGrid.objects.create(is_active=True)
        self.inactive_grid = BingoGrid.objects.create()

        self.challenges = []
        for i in range(16):
            c = Challenge.objects.create(
                name=f"Challenge {i}",
                description=f"Description {i}",
                challenge_type="act",
                points=5
            )
            self.challenges.append(c)
        self.active_grid.challenges.add(*self.challenges)

        self.user = User.objects.create_user(
            username="user1", email="user1@example.com", password="password")

        self.completed_challenge = TileInteraction.objects.create(
            user=self.user, grid=self.active_grid, position=0, completed=True)
        self.started_challenge = TileInteraction.objects.create(
            user=self.user, grid=self.active_grid, position=10)

    def test_get_active_bingo_grid(self):
        # Test that the view will return the active grid.
        bingo_grid = self.client.get(reverse('get_bingo_grid'))
        self.assertEqual(
            bingo_grid.data['grid_id'], self.active_grid.grid_id)

    def test_16_challenges(self):
        # Test that the view returns 16 challenges.
        bingo_grid = self.client.get(reverse('get_bingo_grid'))
        self.assertEqual(
            len(bingo_grid.data['challenges']), 16
        )

    def test_challenge_order(self):
        # Test challenge order is preserved by view.
        bingo_grid = self.client.get(reverse('get_bingo_grid'))
        self.assertEqual(
            bingo_grid.data['challenges'][0]['name'],
            self.challenges[0].name
        )
        self.assertEqual(
            bingo_grid.data['challenges'][10]['name'],
            self.challenges[10].name
        )

    def test_completion_status(self):
        self.client.force_authenticate(user=self.user)

        bingo_grid = self.client.get(reverse('get_bingo_grid'))
        self.assertEqual(
            bingo_grid.data['challenges'][self.completed_challenge.position]['status'], "completed")
        self.assertEqual(
            bingo_grid.data['challenges'][self.started_challenge.position]['status'], "started")
        self.assertEqual(
            bingo_grid.data['challenges'][15]['status'], "not started")
