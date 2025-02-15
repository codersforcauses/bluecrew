from django.test import TestCase
from ..models import User, Challenge, BingoGrid
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class BingoGridUpdateTest(TestCase):
    def setUp(self):
        self.ordinary_user = User.objects.create_user(
            username="user", email="ordinary@example.com", password="password")
        self.superuser = User.objects.create_superuser(
            username="superuser", email="admin@example.com", password="password")

        self.client = APIClient()

        self.challenges = []
        for i in range(20):
            self.challenges.append(Challenge.objects.create(
                name=f"challenge_{i}", challenge_type="act", points=(i*10)))

        self.valid_ids = [c.id for c in self.challenges]

        self.initial_grid = BingoGrid.objects.create(is_active=True)
        self.initial_grid.challenges.add(*(self.challenges[:16]))
        self.valid_request_data = {"challenges": self.valid_ids[4:20]}

    def test_unauthenticated(self):
        response = self.client.post(
            reverse("update-bingo-grid"), self.valid_request_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin(self):
        self.client.force_authenticate(user=self.ordinary_user)
        response = self.client.post(
            reverse("update-bingo-grid"), self.valid_request_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sucessful_update(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            reverse("update-bingo-grid"), self.valid_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_grid = BingoGrid.objects.get(is_active=True)
        # check that a new grid has indeed been created
        self.assertNotEqual(new_grid.grid_id, self.initial_grid.grid_id)

    # helper function
    def _test_active_grid_unchanged(self):
        active_grid = BingoGrid.objects.get(is_active=True)
        return active_grid.grid_id == self.initial_grid.grid_id

    def test_too_few_challenges(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            reverse("update-bingo-grid"), {"challenges": self.valid_ids[:10]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self._test_active_grid_unchanged())

    def test_too_many_challenges(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            reverse("update-bingo-grid"), {"challenges": self.valid_ids[:20]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self._test_active_grid_unchanged())

    def test_invalid_challenge_id(self):
        invalid_id_list = self.valid_ids[:15] + [1 + max(self.valid_ids)]
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            reverse("update-bingo-grid"), {"challenges": invalid_id_list})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self._test_active_grid_unchanged())

    def test_duplicate_challenge_id(self):
        id_list_with_duplicate = self.valid_ids[:15] + [self.valid_ids[0]]
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            reverse("update-bingo-grid"), {"challenges": id_list_with_duplicate})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self._test_active_grid_unchanged())
