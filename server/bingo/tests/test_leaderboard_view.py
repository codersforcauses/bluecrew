from django.test import TestCase
from rest_framework.test import APIClient
from ..models import User


class LeaderboardTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password", total_points=1)
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password", total_points=1)
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password", total_points=3)

        self.client = APIClient()

    def test_leaderboard(self):
        # GET leaderboard api
        leaderboard_response = self.client.get("/api/leaderboard/")
        leaderboard_response_content = leaderboard_response.data

        self.assertEqual(
            leaderboard_response_content[0]["username"], self.user3.username)
        self.assertEqual(
            leaderboard_response_content[0]["total_points"], self.user3.total_points)
        self.assertEqual(leaderboard_response_content[0]["rank"], 1)

        self.assertEqual(
            leaderboard_response_content[1]["username"], self.user1.username)
        self.assertEqual(
            leaderboard_response_content[1]["total_points"], self.user1.total_points)
        self.assertEqual(leaderboard_response_content[1]["rank"], 2)

        self.assertEqual(
            leaderboard_response_content[2]["username"], self.user2.username)
        self.assertEqual(
            leaderboard_response_content[2]["total_points"], self.user2.total_points)
        self.assertEqual(leaderboard_response_content[2]["rank"], 2)

    def test_logged_in_leaderboard(self):
        self.client.force_authenticate(user=self.user1)

        # GET leaderboard api
        leaderboard_response = self.client.get("/api/leaderboard/")
        leaderboard_response_content = leaderboard_response.data

        # last in leaderboard should be current logged in user
        self.assertEqual(
            leaderboard_response_content[-1]["username"], self.user1.username)
        self.assertEqual(
            leaderboard_response_content[-1]["total_points"], self.user1.total_points)
        self.assertEqual(leaderboard_response_content[-1]["rank"], 2)

    def test_exclude_users(self):
        self.superuser = User.objects.create_user(
            username="admin", email="admin@example.com", password="password", total_points=10, is_superuser=True)
        self.inactive_user = User.objects.create_user(
            username="inactive", email="inactive@example.com", password='password', total_points=20, is_active=False)

        leaderboard_response = self.client.get("/api/leaderboard/")
        leaderboard_response_content = leaderboard_response.data

        # Only the 3 normal users should be in this.
        self.assertNotEqual(len(leaderboard_response_content), 5)
        self.assertNotEqual(
            leaderboard_response_content[0]["username"], self.inactive_user.username)
        self.assertNotEqual(
            leaderboard_response_content[1]["username"], self.superuser.username)
