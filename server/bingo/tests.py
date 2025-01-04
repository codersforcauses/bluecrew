from django.test import TestCase, Client
from django.db.utils import IntegrityError
from .models import User, Challenge, Friendship, BingoGrid

from django.core.exceptions import ValidationError


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


class BingoGridTest(TestCase):
    def setUp(self):
        # Create 2 real challenges and 14 dummy ids to test with
        self.challenge1 = Challenge.objects.create(
            name="Real Challenge 1",
            description="Real test challenge #1",
            challenge_type="act",
            points=5,
        )
        self.challenge2 = Challenge.objects.create(
            name="Real Challenge 2",
            description="Real test challenge #2",
            challenge_type="connect",
            points=10,
        )

    def test_create_bingo_grid_with_part_dummy_ids(self):
        # Use 2 real challenge IDs + 14 placeholders
        real_ids = [self.challenge1.id, self.challenge2.id]
        placeholder_ids = [0] * 14

        all_challenge_ids = real_ids + placeholder_ids

        grid = BingoGrid.objects.create(challenges=all_challenge_ids)
        self.assertEqual(len(grid.challenges), 16)
        self.assertEqual(grid.challenges[0], self.challenge1.id)
        self.assertEqual(grid.challenges[1], self.challenge2.id)
        self.assertTrue(all(x == 0 for x in grid.challenges[2:]))

    def test_only_one_active_grid(self):
        # Validate that only one BingoGrid can be active at a time.

        # Create an active grid but with no name so flake doesn't complain
        _ = BingoGrid.objects.create(
            challenges=[self.challenge1.id] + [0]*15,
            is_active=True
        )
        grid2 = BingoGrid(
            challenges=[self.challenge2.id] + [0]*15,
            is_active=True
        )

        with self.assertRaises(ValidationError):
            grid2.full_clean()  # calls .clean(), which should fail

        # If we switch the second grid to inactive, it should pass
        grid2.is_active = False
        grid2.full_clean()
        grid2.save()
        self.assertFalse(grid2.is_active)

    def test_str_representation(self):
        """
        Test the __str__ output, e.g. "BingoGrid #1 (Active: True/False)"
        """
        grid = BingoGrid.objects.create(
            challenges=[self.challenge1.id] + [0]*15,
            is_active=True
        )
        self.assertIn("BingoGrid #", str(grid))
        self.assertIn("(Active: True)", str(grid))
