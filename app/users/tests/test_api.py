from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USERS_URL = reverse("users:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicAPITest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_sucess(self):
        """
        Test creating user with valid payload is successful
        """
        payload = {
            "email": "test@test.com",
            "password": "testpassword",
            "name": "Test Name",
        }

        response = self.client.post(CREATE_USERS_URL, payload)
        user = get_user_model().objects.get(**response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_password_too_short(self):
        """
        Test that password must be more than 5 characters
        """
        payload = {
            "email": "test@test.com",
            "password": "pass",
            "name": "Test Name",
        }

        response = self.client.post(CREATE_USERS_URL, payload)
        user_exists = (
            get_user_model()
            .objects.filter(
                email=payload["email"],
            )
            .exists()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_user_exists(self):
        """
        Test creating user that already exists fails
        """
        payload = {
            "email": "test@test.com",
            "password": "testpassword",
            "name": "Test Name",
        }

        create_user(**payload)
        response = self.client.post(CREATE_USERS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
