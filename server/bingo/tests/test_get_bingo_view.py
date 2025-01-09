from django.test import TestCase
from rest_framework.test import APIClient
from ..models import BingoGrid
from django.urls import reverse


class GetBingoGridTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.activeGrid = BingoGrid.objects.create(is_active=True)
        self.inactiveGrid = BingoGrid.objects.create()

    def test_get_active_bingo_grid(self):
        # Test that the view will return the active grid.
        bingo_grid = self.client.get(reverse('get_bingo_grid'))
        self.assertEqual(
            bingo_grid.data['grid_id'], self.activeGrid.grid_id)
