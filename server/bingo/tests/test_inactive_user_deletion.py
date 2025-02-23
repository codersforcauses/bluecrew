from django.test import TestCase
from django.core.management import call_command
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
                username="user5", password="verysecure123", email="email5@example.com", is_active=False)
        self.new_active_user = User.objects.create(
            username="user6", password="verysecure123", email="email6@example.com", is_active=False)

    def test_deletion_result(self):
        delete_inactive()
        # The only user who should be deleted is the user created more than one day ago who is inactive
        self.assertEqual(set(u.username for u in User.objects.all()), {
                         "user2", "user3", "user4", "user5", "user6"})
