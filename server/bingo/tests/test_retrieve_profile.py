from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import User, Challenge, BingoGrid, TileInteraction, Friendship
from datetime import datetime, timezone


class ProfilePageViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='password123',
            email="testuser1@email.com",
            first_name='John',
            last_name='Doe',
            bio='Test bio',
            visibility=1,
            total_points=15,
            avatar=1
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email="testuser2@email.com",
            password='password123'
        )
        self.user3 = User.objects.create_user(
            username='testuser3',
            email="testuser3@email.com",
            password='password123'
        )
        self.friendship12 = Friendship.objects.create(
            requester=self.user1, receiver=self.user2
        )
        self.grid = BingoGrid.objects.create()

        self.challenges = []
        for i in range(16):
            c = Challenge.objects.create(
                name=f"Challenge {i}",
                description=f"Description {i}",
                challenge_type="act",
                points=5
            )
            self.challenges.append(c)
        self.grid.challenges.add(*self.challenges)

        self.tile_interaction1 = TileInteraction.objects.create(
            user=self.user1,
            grid=self.grid,
            position=0,
            image='/path/to/image1.png',
            date_completed=datetime(
                2025, 1, 18, 11, 0, tzinfo=timezone.utc)
            # No date started since it's automatically set to current time
        )
        self.tile_interaction2 = TileInteraction.objects.create(
            user=self.user1,
            grid=self.grid,
            position=1,
            image='/path/to/image2.png',
            date_completed=datetime(
                2025, 1, 18, 11, 0, tzinfo=timezone.utc)
        )

    def test_get_profile_page_success(self):
        # Authenticate the requesting user (friend of the profile owner)
        self.client.force_authenticate(user=self.user2)

        # Get the profile page
        url = reverse('get_profile_page', kwargs={'username': 'testuser1'})
        response = self.client.get(url)

        # Assert response details
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_info']['first_name'], 'John')
        self.assertEqual(response.data['user_info']['last_name'], 'Doe')
        self.assertEqual(response.data['user_info']['bio'], 'Test bio')
        self.assertEqual(response.data['user_info']['total_points'], 15)
        self.assertEqual(response.data['user_info']['avatar'], 1)

        # Verify challenges details
        challenges = response.data['challenges']
        self.assertEqual(len(challenges), 2)

        # Check first challenge
        challenge1 = challenges[0]
        self.assertEqual(challenge1['name'], 'Challenge 0')
        self.assertEqual(challenge1['description'], 'Description 0')
        self.assertEqual(challenge1['challenge_type'], 'act')
        self.assertEqual(challenge1['points'], 5)
        self.assertEqual(challenge1['image'], '/path/to/image1.png')
        self.assertEqual(challenge1['date_completed'], '2025-01-18T11:00:00Z')

        # Check second challenge
        challenge2 = challenges[1]
        self.assertEqual(challenge2['name'], 'Challenge 1')
        self.assertEqual(challenge2['description'], 'Description 1')
        self.assertEqual(challenge2['challenge_type'], 'act')
        self.assertEqual(challenge2['points'], 5)
        self.assertEqual(challenge2['image'], '/path/to/image2.png')
        self.assertEqual(challenge2['date_completed'], '2025-01-18T11:00:00Z')
