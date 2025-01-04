from django.test import TestCase
from ..models import User, Friendship
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient


class DeleteFriendshipTest(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password")
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password")

        # Create a friendship between user1 and user2
        self.friendship = Friendship.objects.create(
            requester=self.user1, receiver=self.user2)

        # Set up API client
        self.client = APIClient()
        self.delete_friendship_url = reverse(
            'delete_friendship', args=[self.friendship.id])

    def test_delete_friendship_as_requester(self):
        self.client.force_authenticate(
            user=self.user1)  # Authenticate as user1
        response = self.client.delete(self.delete_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Friendship.objects.filter(
            id=self.friendship.id).exists())

    def test_delete_friendship_as_receiver(self):
        self.client.force_authenticate(
            user=self.user2)  # Authenticate as user2
        response = self.client.delete(self.delete_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Friendship.objects.filter(
            id=self.friendship.id).exists())

    def test_delete_friendship_as_non_participant(self):
        self.client.force_authenticate(
            user=self.user3)  # Authenticate as user3
        response = self.client.delete(self.delete_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_friendship_unauthenticated(self):
        response = self.client.delete(self.delete_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_nonexistent_friendship(self):
        self.client.force_authenticate(
            user=self.user1)  # Authenticate as user1
        nonexistent_url = reverse('delete_friendship', args=[999])
        response = self.client.delete(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
