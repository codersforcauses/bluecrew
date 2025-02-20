from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from ..models import User
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs
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
            birthdate=date(1, 1, 1),
            is_active=False
        )

    def test_request_verification(self):
        response = self.client.post(
            reverse("request_verification"),
            {"email": self.user.email}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, settings.ACCOUNTS_EMAIL)
        self.assertEqual(mail.outbox[0].recipients()[0], self.user.email)

        id_parser = FindHREFByID("verify_link")
        id_parser.feed(mail.outbox[0].body)
        url = id_parser.href
        self.assertNotEqual(url, None, "Link was not found in email content")

        query = parse_qs(urlparse(url).query)
        self.assertIn("uid64", query.keys())
        self.assertIn("token", query.keys())

        response = self.client.post(reverse("confirm_email"), query)
        self.assertEqual(response.status_code, 200)
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
        self.client.post(reverse("request_verification"),
                         {"email": self.user.email})
        id_parser = FindHREFByID("verify_link")
        id_parser.feed(mail.outbox[0].body)
        url = id_parser.href
        query = parse_qs(urlparse(url).query)
        response = self.client.post(reverse("confirm_email"), query)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("confirm_email"), query)
        self.assertEqual(response.status_code, 200)

    def test_invalid_UID(self):
        response = self.client.post(
            reverse("confirm_email"),
            {"uid64": "0", "token": "4"}
        )
        self.assertEqual(response.status_code, 400)

    def test_unused_UID(self):
        response = self.client.post(
            reverse("confirm_email"),
            {"uid64": urlsafe_base64_encode(
                force_bytes(self.user.pk+1)), "token": "4"}
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_token(self):
        response = self.client.post(
            reverse("confirm_email"),
            {"uid64": urlsafe_base64_encode(
                force_bytes(self.user.pk)), "token": "42"}
        )
        self.assertEqual(response.status_code, 404)


class TestPasswordReset(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="Test",
            password="A generic valid password",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            birthdate=date(1, 1, 1),
            is_active=True,
        )

    def test_request_reset(self):
        response = self.client.post(
            reverse("request_password_reset"),
            {"email": self.user.email}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, settings.ACCOUNTS_EMAIL)
        self.assertEqual(mail.outbox[0].recipients()[0], self.user.email)

        id_parser = FindHREFByID("reset_link")
        id_parser.feed(mail.outbox[0].body)
        url = id_parser.href
        self.assertNotEqual(url, None, "Link was not found in email content")

        query = parse_qs(urlparse(url).query)
        self.assertIn("uid64", query.keys())
        self.assertIn("token", query.keys())

        response = self.client.post(
            reverse("reset_password"),
            {"uid64": query["uid64"], "token": query["token"],
                "password": "Is this a good password?"}
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Is this a good password?"))

    def test_invalid_email(self):
        response = self.client.post(
            reverse("request_password_reset"),
            {"email": "nobody@someone-else.com"}
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_uid(self):
        response = self.client.post(
            reverse("reset_password"),
            {"uid64": urlsafe_base64_encode(force_bytes(
                self.user.pk+1)), "token": "42", "password": "Is this a good password?"}
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_password(self):
        self.client.post(
            reverse("request_password_reset"),
            {"email": self.user.email}
        )
        id_parser = FindHREFByID("reset_link")
        id_parser.feed(mail.outbox[0].body)
        url = id_parser.href
        query = parse_qs(urlparse(url).query)
        response = self.client.post(
            reverse("reset_password"),
            {"uid64": query["uid64"],
                "token": query["token"], "password": "No."}
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_token(self):
        self.client.post(
            reverse("request_password_reset"),
            {"email": self.user.email}
        )
        id_parser = FindHREFByID("reset_link")
        id_parser.feed(mail.outbox[0].body)
        url = id_parser.href
        query = parse_qs(urlparse(url).query)
        response = self.client.post(
            reverse("reset_password"),
            {"uid64": query["uid64"], "token": "AAAA",
                "password": "Is this a good password?"}
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_params(self):
        response = self.client.post(reverse("reset_password"))
        self.assertEqual(response.status_code, 400)

    def test_weird_uid(self):
        response = self.client.post(reverse("reset_password"), {
                                    "uid64": "14", "token": "AAAA", "password": "Is this a good password?"})
        self.assertEqual(response.status_code, 400)
