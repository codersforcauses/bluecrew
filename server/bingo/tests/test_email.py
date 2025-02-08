from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from ..models import User
from datetime import date
from html.parser import HTMLParser


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

        id_parser = FindHREFByID("verify_link")
        id_parser.feed(mail.outbox[0].body)
        link = id_parser.href

        self.assertNotEqual(link, None, "Link was not found in email content")

        '''response = self.client.get(
            reverse("confirm_email"),
            {}
        )'''
