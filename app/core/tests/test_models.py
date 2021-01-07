from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Tag


def sample_user(email="test@test.com", password="testpassword"):
    """
    Create a sample user
    """
    return get_user_model().objects.create_user(email, password)


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

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                "testpassword",
            )

    def test_create_new_superuser(self):
        """
        Test creating a new superuser
        """
        user = get_user_model().objects.create_superuser(
            "superuser@test.com",
            "superpassword",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """
        Test the tag string representation
        """
        tag = Tag.objects.create(
            user=sample_user(),
            name="Test",
        )

        self.assertEqual(str(tag), tag.name)
