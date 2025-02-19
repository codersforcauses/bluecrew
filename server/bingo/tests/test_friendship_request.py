from django.test import TestCase
from ..models import User, Friendship
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class RequestFriendshipTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password")
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password")
        self.client = APIClient()

    def test_request_friendship_success(self):
        self.client.force_authenticate(user=self.user1)
        request_friendship_url = reverse(
            'request_friendship', args=[self.user2.user_id])
        response = self.client.post(request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"],
                         "Friendship request sent successfully.")
        try:
            friendship = Friendship.objects.get(
                requester=self.user1, receiver=self.user2)
            self.assertEqual(friendship.status, Friendship.PENDING)
        except ObjectDoesNotExist:
            self.fail("Friendship object was not created as expected.")

    def test_request_friendship_to_self(self):
        self.client.force_authenticate(user=self.user1)
        request_friendship_url = reverse(
            'request_friendship', args=[self.user1.user_id])
        response = self.client.post(request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Requester and receiver cannot be the same user.")

    def test_request_friendship_as_unauthenticated(self):
        request_friendship_url = reverse(
            'request_friendship', args=[self.user2.user_id])
        response = self.client.post(request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_friendship_already_exists(self):
        self.client.force_authenticate(user=self.user1)
        request_friendship_url = reverse(
            'request_friendship', args=[self.user2.user_id])
        self.friendship = Friendship.objects.create(
            requester=self.user1, receiver=self.user2)
        response = self.client.post(request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"], "Friendship with this Requester and Receiver already exists.")

    def test_request_friendship_to_nonexistent(self):
        self.client.force_authenticate(user=self.user1)
        nonexistent_user_id = 9999
        request_friendship_url = reverse(
            'request_friendship', args=[nonexistent_user_id])
        response = self.client.post(request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_reverse_friendship_exists(self):
        self.client.force_authenticate(user=self.user1)
        request_friendship_url = reverse(
            'request_friendship', args=[self.user2.user_id])

        # create a reverse friendship request (user2 -> user1)
        Friendship.objects.create(
            requester=self.user2, receiver=self.user1, status=Friendship.PENDING)

        response = self.client.post(request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"],
                         "A reverse friendship already exists.")

    def test_request_inactive_user_fail(self):
        # Test that an inactive user cannot receive friendship requests.
        self.client.force_authenticate(user=self.user1)
        self.inactive_user = User.objects.create_user(
            username="inactive_user", email="user4@example.com", password="password", is_active=False)
        request_friendship_url = reverse(
            'request_friendship', args=[self.inactive_user.user_id])

        response = self.client.post(request_friendship_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
