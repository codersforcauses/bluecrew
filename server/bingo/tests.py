from django.db.utils import IntegrityError
from django.test import TestCase
from .models import User, Challenge, Friendship
from django.core.exceptions import ValidationError
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient


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
        self.assertEqual(str(challenge), "Challenge 1: Test (Act)")

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
