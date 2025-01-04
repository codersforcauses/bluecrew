from django.test import TestCase, Client
from django.db.utils import IntegrityError
from django.utils import timezone
from .models import User, Challenge, Friendship, ChallengeInteraction

from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class ChallengeTest(TestCase):
    def setUp(self):
        Challenge.objects.create(
            name="Test",
            description="This is a test challenge.",
            challenge_type="act",
            points=5,
            total_completions=10,
        )

    def test_create_challenge(self):
        challenge = Challenge.objects.get(name="Test")
        self.assertEqual(challenge.description, "This is a test challenge.")
        self.assertEqual(challenge.challenge_type, "act")
        self.assertEqual(challenge.points, 5)
        self.assertEqual(challenge.total_completions, 10)
        # Build expected string around challenge rather than hard coded id
        expected_str = f"Challenge {challenge.id}: {challenge.name} ({challenge.challenge_type.capitalize()})"
        self.assertEqual(str(challenge), expected_str)

    def test_invalid_challenge_type(self):
        challenge = Challenge(
            name="Invalid Type Test",
            description="Challenge with an invalid type.",
            challenge_type="invalid_type",  # invalid value
            points=10,
        )
        with self.assertRaises(ValidationError):
            challenge.full_clean()  # validates the model instance before saving to db

    def test_default_total_completions(self):
        challenge = Challenge.objects.create(
            name="Default Completions Test",
            description="Challenge without specifying total_completions.",
            challenge_type="connect",
            points=15,
        )
        self.assertEqual(challenge.total_completions, 0)


class RegisterUserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_user(self):
        response = self.client.post(
            '/api/register/', {'username': 'test_user', 'email': 'test@gmail.com',
                               'first_name': 'larry', 'last_name': 'bird', 'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 201)

    # Required fields not sent.
    def test_register_user_error(self):
        response = self.client.post(
            '/api/register/', {'username': 'forgotten_fields', 'email': 'test@gmail.com',
                               'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_email_error(self):
        response = self.client.post(
            '/api/register/', {'username': 'forgotten_fields', 'email': 'invalidemail',
                               'first_name': 'larry', 'last_name': 'bird', 'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 400)

    def test_insecure_password_error(self):
        response = self.client.post(
            '/api/register/', {'username': 'forgotten_fields', 'email': 'test@test.com',
                               'first_name': 'larry', 'last_name': 'bird', 'password': '1234'}
        )

        self.assertEqual(response.status_code, 400)


class FriendshipTest(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password")
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password")

    def test_create_friendship(self):
        # Tests whether a frienship can be created
        friendship = Friendship.objects.create(
            requester=self.user1, receiver=self.user2)
        self.assertEqual(friendship.requester, self.user1)
        self.assertEqual(friendship.receiver, self.user2)
        # Checks default status is pending
        self.assertEqual(friendship.status, Friendship.PENDING)

    def test_unique_together_constraint(self):
        # Create a friendship
        Friendship.objects.create(requester=self.user1, receiver=self.user2)

        # Attempt to create a duplicate friendship
        with self.assertRaises(IntegrityError):
            Friendship.objects.create(
                requester=self.user1, receiver=self.user2)

    def test_status_choices(self):
        # Test creating a friendship with "accepted" status
        friendship = Friendship.objects.create(
            requester=self.user1, receiver=self.user2, status=Friendship.ACCEPTED)
        self.assertEqual(friendship.status, Friendship.ACCEPTED)

        # Test invalid status
        with self.assertRaises(ValidationError):
            Friendship.objects.create(
                requester=self.user1, receiver=self.user3, status="invalid").full_clean()

    def test_str_representation(self):
        # Test the string representation of a friendship
        friendship = Friendship.objects.create(
            requester=self.user1, receiver=self.user2)
        expected_str = f"Friend request from {
            self.user1} to {self.user2} (Pending)"
        self.assertEqual(str(friendship), expected_str)

    def test_delete_user_cascades(self):
        # Test that deleting a user cascades to related friendships
        Friendship.objects.create(requester=self.user1, receiver=self.user2)
        self.user1.delete()
        self.assertEqual(Friendship.objects.count(), 0)

    def test_reverse_friendship(self):
        # Test whether two reverse friendship can be created
        Friendship.objects.create(requester=self.user1, receiver=self.user2)

        with self.assertRaises(ValidationError):
            Friendship.objects.create(
                requester=self.user2, receiver=self.user1).full_clean()

    def test_friends_with_self(self):
        # Test that a user cannot have a friendship with themselves
        with self.assertRaises(ValidationError):
            Friendship.objects.create(
                requester=self.user1, receiver=self.user1).full_clean()


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
        response = self.client.get(reverse("current-user"))

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
        self.assertEqual(response.data["visibility"], self.user.visibility)  # Using PUBLIC (2)
        self.assertEqual(response.data["avatar"], self.user.avatar)

    def test_get_current_user_unauthenticated(self):
        """Test getting current user details when not authenticated"""
        response = self.client.get(reverse("current-user"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_current_user_method_not_allowed(self):
        """Test that only GET method is allowed"""
        self.client.force_authenticate(user=self.user)

        # Test POST request
        response = self.client.post(reverse("current-user"), {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test PUT request
        response = self.client.put(reverse("current-user"), {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test DELETE request
        response = self.client.delete(reverse("current-user"))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ChallengeInteractionTest(TestCase):
    def setUp(self):
        # Create a user and a challenge to be used by the tests.
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        self.challenge = Challenge.objects.create(
            name="Testing Challenge",
            description="Challenge for testing interactions",
            challenge_type="act",
            points=5,
        )

    def test_create_challenge_interaction(self):
        # Test that a ChallengeInteraction can be created successfully.
        interaction = ChallengeInteraction.objects.create(
            user=self.user,
            challenge=self.challenge
        )
        self.assertFalse(interaction.completed)
        self.assertFalse(interaction.consent)
        self.assertIsNotNone(interaction.date_started)
        self.assertIsNone(interaction.date_completed)
        # For now test that image is "empty"
        self.assertFalse(interaction.image)

    def test_complete_challenge(self):
        # Test updating the 'completed' status and setting 'date_completed'.
        interaction = ChallengeInteraction.objects.create(
            user=self.user,
            challenge=self.challenge
        )

        # simulate completion
        interaction.completed = True
        interaction.date_completed = timezone.now()
        interaction.save()

        updated_interaction = ChallengeInteraction.objects.get(pk=interaction.pk)
        self.assertTrue(updated_interaction.completed)
        self.assertIsNotNone(updated_interaction.date_completed)

    def test_consent(self):
        # Test that 'consent' can be updated appropriately.
        interaction = ChallengeInteraction.objects.create(
            user=self.user,
            challenge=self.challenge
        )
        # Initially false
        self.assertFalse(interaction.consent)
        # Update
        interaction.consent = True
        interaction.save()

        updated_interaction = ChallengeInteraction.objects.get(pk=interaction.pk)
        self.assertTrue(updated_interaction.consent)
