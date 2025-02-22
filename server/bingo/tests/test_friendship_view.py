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

    def test_get_all_friends_data_authenticated(self):
        """Test getting all friends data when authenticated"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('all_friends_data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check structure of response
        self.assertIn('current_friends', response.data)
        self.assertIn('incoming_requests', response.data)
        self.assertIn('outgoing_requests', response.data)
        # Check counts
        self.assertEqual(len(response.data['current_friends']), 1)
        self.assertEqual(len(response.data['incoming_requests']), 1)
        self.assertEqual(len(response.data['outgoing_requests']), 1)
        # Check specific data
        self.assertEqual(response.data['current_friends'][0]['userName'], 'user2')
        self.assertEqual(response.data['incoming_requests'][0]['userName'], 'user4')
        self.assertEqual(response.data['outgoing_requests'][0]['userName'], 'user3')

    def test_get_all_friends_data_unauthenticated(self):
        """Test getting all friends data when not authenticated"""
        response = self.client.get(reverse('all_friends_data'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_friends_or_requests(self):
        """Test getting all friends data when user has no friends or requests"""
        lonely_user = User.objects.create_user(
            username="lonely",
            password="testpass123",
            email="lonely@example.com"
        )
        self.client.force_authenticate(user=lonely_user)
        response = self.client.get(reverse('all_friends_data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['current_friends']), 0)
        self.assertEqual(len(response.data['incoming_requests']), 0)
        self.assertEqual(len(response.data['outgoing_requests']), 0)

    def test_method_not_allowed(self):
        """Test that only GET method is allowed"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('all_friends_data')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
