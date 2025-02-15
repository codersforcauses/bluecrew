from django.test import TestCase, Client


class RegisterUserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_user(self):
        response = self.client.post(
            '/api/register/', {'username': 'test_user', 'email': 'test@gmail.com',
                               'first_name': 'larry', 'last_name': 'bird', 'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 201)

    # Required fields not sent.
    def test_register_user_error(self):
        response = self.client.post(
            '/api/register/', {'username': 'forgotten_fields',
                               'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_email_error(self):
        response = self.client.post(
            '/api/register/', {'username': 'forgotten_fields', 'email': 'invalidemail',
                               'first_name': 'larry', 'last_name': 'bird', 'password': 'SuperSecure123'}
        )

        self.assertEqual(response.status_code, 400)

    def test_insecure_password_error(self):
        response = self.client.post(
            '/api/register/', {'username': 'forgotten_fields', 'email': 'test@test.com',
                               'first_name': 'larry', 'last_name': 'bird', 'password': '1234'}
        )

        self.assertEqual(response.status_code, 400)

    def test_username_restriction(self):
        # Test special characters not allowed in username.
        response = self.client.post(
            '/api/register/', {'username': '////@@!!', 'email': 'test@test.com',
                               'first_name': 'larry', 'last_name': 'bird', 'password': 'Password!!@@1234'}
        )
        self.assertEqual(response.status_code, 400)
