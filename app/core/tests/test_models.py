from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_create_user_with_email_sucessful(self):
        """
        Test creating a new user with an email is sucessful
        """
        email = "test@test.com"
        password = "testpassword"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        email = "test@TEST.COM"
        password = "randompassword"
        user = get_user_model().objects.create_user(
            email,
            password,
        )

        self.assertEqual(user.email, email.lower())
