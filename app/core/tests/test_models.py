"""
Test the App DB Models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """ Test Models """

    def test_create_user_with_email_successful(self):
        """ Test Create User with Email successful """

        email = 'test@example.com'
        password = 'testpassword'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """ Normalize new users email """

        sample_emails = [
            ["test@EXAMPLE.com", "test@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            """ Test Normalized Data """

            user = get_user_model().objects.create_user(email, 'sample123')

            self.assertEqual(user.email, expected)

    def test_user_without_email_address(self):
        """ Test users without email address """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """ Test creating a superuser """

        email = 'test@example.com'
        password = 'testpassword'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
