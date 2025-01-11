from django.test import TestCase
from ..models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class CurrentUserViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            bio="Test bio",
            total_points=100,
            visibility=User.Visibility.PUBLIC,  # This is 2 for PUBLIC
            avatar=1,
        )
        # Initialize the API client
        self.client = APIClient()

    def test_get_current_user_authenticated(self):
        """Test getting current user details when authenticated"""
        # Force authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make request to the endpoint
        response = self.client.get(reverse("current_user"))

        # Check response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response data matches expected TypeScript interface
        self.assertEqual(response.data["userId"], self.user.user_id)
        self.assertEqual(response.data["userName"], self.user.username)
        self.assertEqual(response.data["firstName"], self.user.first_name)
        self.assertEqual(response.data["lastName"], self.user.last_name)
        self.assertEqual(response.data["bio"], self.user.bio)
        self.assertEqual(response.data["totalPoints"], self.user.total_points)
        self.assertEqual(response.data["email"], self.user.email)
        # Using PUBLIC (2)
        self.assertEqual(response.data["visibility"], self.user.visibility)
        self.assertEqual(response.data["avatar"], self.user.avatar)

    def test_get_current_user_unauthenticated(self):
        """Test getting current user details when not authenticated"""
        response = self.client.get(reverse("current_user"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_current_user_method_not_allowed(self):
        """Test that only GET method is allowed"""
        self.client.force_authenticate(user=self.user)

        # Test POST request
        response = self.client.post(reverse("current_user"), {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test PUT request
        response = self.client.put(reverse("current_user"), {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test DELETE request
        response = self.client.delete(reverse("current_user"))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
