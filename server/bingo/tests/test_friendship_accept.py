from django.test import TestCase
from ..models import User, Friendship
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class AcceptFriendshipTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password")
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password")

        self.client = APIClient()
        self.friendship = Friendship.objects.create(requester=self.user1, receiver=self.user2)
        self.accept_friendship_url = reverse('accept_friendship', args=[self.friendship.id])

    def test_accept_request_as_requester(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.accept_friendship_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # refresh friendship obj to get latest data from db
        self.friendship.refresh_from_db()
        self.assertEqual(self.friendship.status, Friendship.PENDING)

    def test_accept_request_as_receiver(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.accept_friendship_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.friendship.refresh_from_db()
        self.assertEqual(self.friendship.status, Friendship.ACCEPTED)

    def test_accept_friendship_as_non_participant(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.post(self.accept_friendship_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.friendship.refresh_from_db()
        self.assertEqual(self.friendship.status, Friendship.PENDING)

    def test_accept_friendship_unauthenticated(self):
        response = self.client.post(self.accept_friendship_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accept_nonexistent_friendship(self):
        self.client.force_authenticate(user=self.user1)
        nonexistent_url = reverse('accept_friendship', args=[999])
        response = self.client.post(nonexistent_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_accept_already_accepted_friendship(self):
        self.friendship.status = Friendship.ACCEPTED
        self.friendship.save()
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.accept_friendship_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Friendship is already accepted.")
        self.friendship.refresh_from_db()
        self.assertEqual(self.friendship.status, Friendship.ACCEPTED)
