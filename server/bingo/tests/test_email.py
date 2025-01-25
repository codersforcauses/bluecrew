from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from ..models import User
from datetime import date


class TestEmailVerification(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="Test",
            password="A generic valid password",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            birthdate=date(1, 1, 1)
        )

    def test_request_verification(self):
        response = self.client.post(
            reverse("request_verification"),
            {"email": self.user.email}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        # link = mail.outbox[0].body
        response = self.client.get(
            reverse("confirm_email"),
            {}
        )
