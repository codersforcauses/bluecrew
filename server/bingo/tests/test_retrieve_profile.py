from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import User, Challenge, BingoGrid, TileInteraction, Friendship


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
            date_started='2025-01-18T10:00:00Z',
            date_completed='2025-01-18T11:00:00Z'
        )
        self.tile_interaction2 = TileInteraction.objects.create(
            user=self.user1,
            grid=self.grid,
            position=1,
            image='/path/to/image2.png',
            date_started='2025-01-18T10:00:00Z',
            date_completed='2025-01-18T11:00:00Z'
        )

    def test_get_profile_page_success(self):
        # Authenticate the requesting user (friend of the profile owner)
        self.client.force_authenticate(user=self.user2)

        # Get the profile page
        url = reverse('get_profile_page', kwargs={'username': 'testuser1'})
        response = self.client.get(url)
        print(response.content)
        print(response.data)

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

        # Check second challenge
        challenge2 = challenges[1]
        self.assertEqual(challenge2['name'], 'Challenge 1')
        self.assertEqual(challenge2['description'], 'Description 1')
        self.assertEqual(challenge2['challenge_type'], 'act')
        self.assertEqual(challenge2['points'], 5)

    # def test_get_profile_page_user_not_found(self):
    #     self.client.force_authenticate(user=self.user2)
    #     url = reverse('get_profile_page', kwargs={
    #                   'username': 'nonexistentuser'})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data['error'], 'User not found')

    # def test_get_profile_page_access_denied(self):
    #     # Attempt to access user1's profile with user3 (not a friend)
    #     self.client.force_authenticate(user=self.user3)
    #     url = reverse('get_profile_page', kwargs={'username': 'testuser1'})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.data['error'], 'Access denied')

    # def test_get_profile_page_unauthenticated(self):
    #     url = reverse('get_profile_page', kwargs={'username': 'testuser1'})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
