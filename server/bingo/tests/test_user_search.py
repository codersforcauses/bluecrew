from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import User, Friendship


class UserSearchTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.current_user = User.objects.create_user(
            username='larrybird', email='lbird@celtics.com', password='ChampsHere123')
        self.url = reverse('user_search')

        self.user1 = User.objects.create_user(
            username='lebronjames', email='lbj@lakers.com', password='AkronHammer123')
        self.user2 = User.objects.create_user(
            username='lebronjamesjr', email='bronny@lakers.com', password='password123')
        self.user3 = User.objects.create_user(
            username='lebronjamesfanpage', email='lbj@gmail.com', password='3-1comeback')
        self.user4 = User.objects.create_user(
            username='lbjking', email='lbj@cavs.com', password='forgottenAccount'
        )

        self.friendship1 = Friendship.objects.create(
            requester=self.current_user, receiver=self.user1, status=Friendship.PENDING)
        self.friendship2 = Friendship.objects.create(
            requester=self.user2, receiver=self.current_user, status=Friendship.PENDING
        )
        self.friendship4 = Friendship.objects.create(
            requester=self.current_user, receiver=self.user4, status=Friendship.ACCEPTED
        )

    def test_friendship_messages(self):
        self.client.force_authenticate(user=self.current_user)
        response = self.client.post(
            self.url, data={'query_string': 'lebronjames'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'],
                         'You have requested friendship.')

        response = self.client.post(
            self.url, data={'query_string': 'lebronjamesjr'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'],
                         'Pending friendship request.')
        self.assertEqual(
            response.data[0]['friendship_id'], self.friendship2.id)
        response = self.client.post(
            self.url, data={'query_string': 'lebronjamesfanpage'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'You are not friends.')

        response = self.client.post(
            self.url, data={'query_string': 'lbjking'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'You are friends.')

    def test_exclude_superuser(self):
        User.objects.create_user(
            username='admin', password='Password123', email='admin@mail.com', is_superuser=True)

        self.client.force_authenticate(user=self.current_user)
        response = self.client.post(
            self.url, data={'query_string': 'admin'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_exclude_inactive(self):
        User.objects.create_user(
            username='inactive_person', password='Password123', email='not_active@mail.com', is_active=False)

        self.client.force_authenticate(user=self.current_user)
        response = self.client.post(
            self.url, data={'query_string': 'inactive'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_exact_match_included(self):
        for i in range(15):
            User.objects.create_user(username=f'uniqueuname{i}',
                                     password='Password123', email=f'user{i}@mail.com')
        self.target_user = User.objects.create_user(
            username='uniqueuname', password='Password123', email='target_user@mail.com')

        self.client.force_authenticate(user=self.current_user)
        response = self.client.post(
            self.url, data={'query_string': 'uniqueuname'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.target_result = {'user_data': {'avatar': self.target_user.avatar, 'username': self.target_user.username,
                                            'user_id': self.target_user.user_id}, 'status': 'You are not friends.'}
        self.assertIn(self.target_result, response.data)
        self.assertEqual(len(response.data), 15)

    def test_no_match_found(self):

        self.client.force_authenticate(user=self.current_user)
        response = self.client.post(
            self.url, data={'query_string': 'uniqueuname'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
