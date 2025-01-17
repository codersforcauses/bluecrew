from django.test import TestCase
from ..models import User, Friendship
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class FriendViewsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="testpass123",
            email="user1@example.com",
            first_name="Test",
            last_name="One"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="testpass123",
            email="user2@example.com",
            first_name="Test",
            last_name="Two"
        )
        self.user3 = User.objects.create_user(
            username="user3",
            password="testpass123",
            email="user3@example.com",
            first_name="Test",
            last_name="Three"
        )
        self.user4 = User.objects.create_user(
            username="user4",
            password="testpass123",
            email="user4@example.com",
            first_name="Test",
            last_name="Four"
        )
        self.client = APIClient()
        self.accepted_friendship = Friendship.objects.create(
            requester=self.user1,
            receiver=self.user2,
            status='accepted'
        )
        self.outgoing_request = Friendship.objects.create(
            requester=self.user1,
            receiver=self.user3,
            status='pending'
        )
        self.incoming_request = Friendship.objects.create(
            requester=self.user4,
            receiver=self.user1,
            status='pending'
        )

    def test_get_friends_authenticated(self):
        """Test getting friends list when authenticated"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('friend_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['userName'], 'user2')

    def test_get_friends_unauthenticated(self):
        """Test getting friends list when not authenticated"""
        response = self.client.get(reverse('friend_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_outgoing_requests_authenticated(self):
        """Test getting outgoing friend requests when authenticated"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('outgoing_requests'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['userName'], 'user3')

    def test_get_outgoing_requests_unauthenticated(self):
        """Test getting outgoing requests when not authenticated"""
        response = self.client.get(reverse('outgoing_requests'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_incoming_requests_authenticated(self):
        """Test getting incoming friend requests when authenticated"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('incoming_requests'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['userName'], 'user4')

    def test_get_incoming_requests_unauthenticated(self):
        """Test getting incoming requests when not authenticated"""
        response = self.client.get(reverse('incoming_requests'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_friends(self):
        """Test getting friends list when user has no friends"""
        lonely_user = User.objects.create_user(
            username="lonely",
            password="testpass123",
            email="lonely@example.com"
        )
        self.client.force_authenticate(user=lonely_user)
        response = self.client.get(reverse('friend_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_friend_list_method_not_allowed(self):
        """Test that only GET method is allowed for friends list"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('friend_list'), {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(reverse('friend_list'), {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(reverse('friend_list'))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
