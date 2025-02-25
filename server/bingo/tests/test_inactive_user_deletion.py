from django.test import TestCase
from bingo.models import User
from freezegun import freeze_time
from django.utils import timezone
from datetime import timedelta
from ..tasks import delete_inactive


class InactiveUserDeletionTestCase(TestCase):
    def setUp(self):
        with freeze_time(timezone.now() - timedelta(days=2)):
            self.old_inactive_user = User.objects.create(
                username="user1", password="verysecure123", email="email1@example.com", is_active=False)
        with freeze_time(timezone.now() - timedelta(hours=1)):
            self.recent_inactive_user = User.objects.create(
                username="user2", password="verysecure123", email="email2@example.com", is_active=False)
        self.new_inactive_user = User.objects.create(
            username="user3", password="verysecure123", email="email3@example.com", is_active=False)
        with freeze_time(timezone.now() - timedelta(days=2)):
            self.old_active_user = User.objects.create(
                username="user4", password="verysecure123", email="email4@example.com")
        with freeze_time(timezone.now() - timedelta(hours=1)):
            self.recent_active_user = User.objects.create(
                username="user5", password="verysecure123", email="email5@example.com")
        self.new_active_user = User.objects.create(
            username="user6", password="verysecure123", email="email6@example.com")

    def test_deletion_result(self):
        delete_inactive()
        # Ensure the old inactive user is deleted
        self.assertFalse(User.objects.filter(
            username="user1").exists(), "Old inactive user was not deleted.")

        # Ensure all other users are still in the database
        remaining_users = set(User.objects.values_list("username", flat=True))
        expected_users = {"user2", "user3", "user4", "user5", "user6"}

        self.assertEqual(remaining_users, expected_users,
                         "Unexpected users were deleted.")
