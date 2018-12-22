from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from allauth.account.models import EmailAddress


def create_user():
    user = User.objects.create_user('alice', 'alice@example.com', 'secret')
    EmailAddress(user=user, verified=True, primary=True).save()
    return user


class LoginTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_front_page_redirects_to_login_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['Location'], '/accounts/login/?next=/')

    def test_login_page_includes_email_and_password_fields(self):
        response = self.client.get('/accounts/login/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('E-mail', response.content)
        self.assertIn('Password', response.content)

    def test_successful_login_redirects_to_front_page(self):
        response = self.client.post(
            '/accounts/login/',
            {'login': 'alice@example.com', 'password': 'secret'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')

    def test_failed_login_shows_error_on_login_page(self):
        response = self.client.post(
            '/accounts/login/',
            {'login': 'alice@example.com', 'password': 'wrong'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'The e-mail address and/or password you specified are not correct.', response.content)
