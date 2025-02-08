from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from ..models import User
from datetime import date
from html.parser import HTMLParser
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class FindHREFByID(HTMLParser):
    def __init__(self, target_id, *, convert_charrefs=True):
        self.target_id = target_id
        self.href = None
        super().__init__(convert_charrefs=convert_charrefs)

    def handle_starttag(self, tag, attrs):
        if ("id", self.target_id) in attrs:
            attr_dict = dict(attrs)
            self.href = attr_dict.get("href")


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
        self.assertEqual(mail.outbox[0].from_email, settings.VERIFICATION_EMAIL)

        id_parser = FindHREFByID("verify_link")
        id_parser.feed(mail.outbox[0].body)
        url = id_parser.href
        self.assertNotEqual(url, None, "Link was not found in email content")

        path = url.split("testserver")[1]

        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_no_email(self):
        response = self.client.post(reverse("request_verification"))
        self.assertEqual(response.status_code, 400)

    def test_already_active(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(
            reverse("request_verification"),
            {"email": self.user.email}
        )
        self.assertEqual(response.status_code, 400)

    def test_repeat_activation(self):
        self.client.post(reverse("request_verification"), {"email": self.user.email})
        id_parser = FindHREFByID("verify_link")
        id_parser.feed(mail.outbox[0].body)
        path = id_parser.href.split("testserver")[1]
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)

    def test_invalid_UID(self):
        response = self.client.get(
            reverse("confirm_email"),
            {"uid64": "0", "token": "4"}
        )
        self.assertEqual(response.status_code, 400)

    def test_unused_UID(self):
        response = self.client.get(
            reverse("confirm_email"),
            {"uid64": urlsafe_base64_encode(force_bytes(self.user.pk+1)), "token": "4"}
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_token(self):
        response = self.client.get(
            reverse("confirm_email"),
            {"uid64": urlsafe_base64_encode(force_bytes(self.user.pk)), "token": "42"}
        )
        self.assertEqual(response.status_code, 404)
