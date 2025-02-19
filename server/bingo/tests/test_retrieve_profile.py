from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import User, Challenge, BingoGrid, TileInteraction, Friendship
from datetime import datetime, timezone


class ProfilePageViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users with different visibility settings
        self.users = {
            'public': self._create_test_user(
                username='public',
                visibility=2,
                first_name='Public',
                avatar=1
            ),
            'friend': self._create_test_user(
                username='friend',
                visibility=1,
                first_name='Friend',
                avatar=2
            ),
            'staff': self._create_test_user(
                username='staff',
                visibility=0,
                first_name='Staff',
                avatar=3
            )
        }

        # Default tile completion date
        self.completion_date = datetime(
            2025, 1, 18, 11, 0, tzinfo=timezone.utc)

        # Create grid and challenges
        self.grid = BingoGrid.objects.create()
        self.challenges = self._create_challenges(16)
        self.grid.challenges.add(*self.challenges)

        # Create tile interactions for each user
        for user in self.users.values():
            self._create_tile_interactions(user, self.grid, 16)

    def _create_test_user(self, username, visibility, first_name, avatar):
        """Helper method to create a test user with standard attributes"""
        return User.objects.create_user(
            username=username,
            password='password123',
            email=f"{username}@email.com",
            first_name=first_name,
            last_name='Test',
            bio='Test bio',
            visibility=visibility,
            total_points=15,
            avatar=avatar
        )

    def _create_challenges(self, count):
        """Helper method to create a specified number of test challenges"""
        return [
            Challenge.objects.create(
                name=f"Challenge {i}",
                description=f"Description {i}",
                challenge_type="act",
                points=5
            ) for i in range(count)
        ]

    def _create_tile_interactions(self, user, grid, count):
        """Helper method to create tile interactions for a user"""
        return [
            TileInteraction.objects.create(
                user=user,
                grid=grid,
                position=i,
                image=f'path/to/image{i}.png',
                date_completed=self.completion_date
            ) for i in range(count)
        ]

    def _assert_basic_user_info(self, response_data, user):
        """Helper method to assert basic user information"""
        user_info = response_data['user_info']
        self.assertEqual(user_info['firstName'], user.first_name)
        self.assertEqual(user_info['lastName'], user.last_name)
        self.assertEqual(user_info['bio'], user.bio)
        self.assertEqual(user_info['totalPoints'], user.total_points)
        self.assertEqual(user_info['avatar'], user.avatar)

    def _assert_challenge_data(self, challenges):
        """Helper method to assert challenge data"""
        self.assertEqual(len(challenges), 16)
        challenge = challenges[0]
        self.assertEqual(challenge['title'], 'Challenge 0')
        self.assertEqual(challenge['description'], 'Description 0')
        self.assertEqual(challenge['type'], 'Act')
        self.assertEqual(challenge['points'], 5)
        self.assertEqual(challenge['image'], '/media/path/to/image0.png')
        self.assertEqual(
            challenge['finishDate'], self.completion_date.strftime("%d/%m/%y %I:%M %p"))

    def _create_generic_user(self):
        new_user = self._create_test_user(
            'generic_user', visibility=2, first_name='New', avatar=1)
        self.client.force_authenticate(user=new_user)

    def _create_friend_user(self):
        new_user = self._create_test_user(
            'friend_user', visibility=2, first_name='New', avatar=1)
        for target_user in self.users.values():
            Friendship.objects.create(
                requester=new_user,
                receiver=target_user,
                status='accepted'
            )
        self.client.force_authenticate(user=new_user)

    def _create_super_user(self):
        new_user = self._create_test_user(
            'super_user', visibility=2, first_name='New', avatar=1)
        new_user.is_superuser = True
        self.client.force_authenticate(user=new_user)

    def test_all_visbility_permissions_pairs(self):
        """
        Tests all access combinations of visibilities and users
        If access (O) is allowed, assert the challenges are correct otherwise (X) assert they are empty

                 | PUBLIC | FRIENDS | STAFF |
        NON-USER |   O    |    X    |   X   |
         GENERIC |   O    |    X    |   X   |
          FRIEND |   O    |    O    |   X   |
           STAFF |   O    |    O    |   O   |

        """
        user_roles = [
            None,  # Unauthenticated user
            self._create_generic_user,  # Regular user
            self._create_friend_user,  # Friend
            self._create_super_user,  # Admin
        ]
        for role_idx, set_current_user in enumerate(user_roles):
            if set_current_user is not None:
                set_current_user()
            for visibility_idx, (username, target_user) in enumerate(self.users.items()):
                response = self.client.get(
                    reverse('get_profile_page', kwargs={
                            'username': username})
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self._assert_basic_user_info(
                    response.data, target_user)
                if role_idx > visibility_idx or (role_idx == 0 and visibility_idx == 0):
                    self._assert_challenge_data(
                        response.data['challenges'])  # Only if have access
                else:
                    # If no access
                    self.assertEqual(len(response.data['challenges']), 0)

    def test_get_non_user(self):
        response = self.client.get(
            reverse('get_profile_page', kwargs={
                'username': 'non_existant_user'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_own_page(self):
        self.client.force_authenticate(user=self.users['friend'])
        response = self.client.get(
            reverse('get_profile_page', kwargs={
                'username': 'friend'})
        )
        self._assert_basic_user_info(
            response.data, self.users['friend']
        )
        self._assert_challenge_data(response.data['challenges'])
