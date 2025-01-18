from django.test import TestCase
from ..models import User, Friendship
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class RequestFrienshipTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password")
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password")
        self.client = APIClient()
        

    def test_create_friendship_success(self):
        self.client.force_authenticate(user=self.user1)
        self.request_friendship_url = reverse('request_friendship', args=[self.user2.user_id])
        response = self.client.post(self.request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Friendship request sent successfully.")
        try:
            Friendship.objects.get(requester=self.user1, receiver=self.user2)
        except ObjectDoesNotExist:
            self.fail("Failed to find friendship")

