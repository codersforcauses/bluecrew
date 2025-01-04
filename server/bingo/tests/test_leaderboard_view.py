from django.test import TestCase, Client
from ..models import User
import json


class LeaderboardTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password", total_points=1)
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password", total_points=1)
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password", total_points=3)

        self.client = Client()

    def test_leaderboard(self):
        # GET leaderboard api
        leaderboard_response = self.client.get("/api/leaderboard", follow=True)
        leaderboard_response_content = json.loads(leaderboard_response.content.decode("utf8"))

        self.assertEqual(leaderboard_response_content[0]["username"], "user3")
        self.assertEqual(leaderboard_response_content[0]["total_points"], 3)
        self.assertEqual(leaderboard_response_content[0]["rank"], 1)

        self.assertEqual(leaderboard_response_content[1]["username"], "user1")
        self.assertEqual(leaderboard_response_content[1]["total_points"], 1)
        self.assertEqual(leaderboard_response_content[1]["rank"], 2)

        self.assertEqual(leaderboard_response_content[2]["username"], "user2")
        self.assertEqual(leaderboard_response_content[2]["total_points"], 1)
        self.assertEqual(leaderboard_response_content[2]["rank"], 2)

    def test_logged_in_leaderboard(self):
        self.client.login(username="user1", password="password")

        # get auth token
        token_response = self.client.post(
            "/api/token/", {"username": "user1", "password": "password"}, content_type="application/json")
        token_response_content = json.loads(
            token_response.content.decode('utf-8'))

        # GET leaderboard api
        user_token = token_response_content["access"]
        leaderboard_response = self.client.get(
            "/api/leaderboard", headers={"Authorization": "Bearer " + user_token}, follow=True)
        leaderboard_response_content = json.loads(
            leaderboard_response.content.decode("utf8"))

        # last in leaderboard should be current logged in user
        self.assertEqual(leaderboard_response_content[-1]["username"], "user1")
        self.assertEqual(leaderboard_response_content[-1]["total_points"], 1)
        self.assertEqual(leaderboard_response_content[-1]["rank"], 2)
