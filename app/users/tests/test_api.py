from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USERS_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")
ME_URL = reverse("users:me")


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

    def test_create_token_for_user(self):
        """
        Test that a token is created for the user
        """
        payload = {
            "email": "test@test.com",
            "password": "testpassword",
        }

        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Test that token is not created if invalid credentials are given
        """
        create_user(
            email="test@test.com",
            password="testpassword",
        )
        payload = {
            "email": "test@test.com",
            "password": "wrongpassword",
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that token is not created if user doesn't exist
        """
        payload = {
            "email": "test@test.com",
            "password": "testpassword",
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test that email and password are required
        """
        response = self.client.post(
            TOKEN_URL,
            {
                "email": "test",
                "password": "",
            },
        )

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for users
        """
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITest(TestCase):
    """
    Test AI requests that require authentication
    """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@test.com",
            password="testpassword",
            name="Test Name",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in user
        """
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "email": self.user.email,
                "name": self.user.name,
            },
        )

    def test_post_me_not_allowed(self):
        """
        Test that POST is not allowed on the me url
        """
        response = self.client.post(ME_URL, {})

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_update_user_profile(self):
        """
        Test updating the user profile for authenticated user
        """
        payload = {
            "name": "New Name",
            "password": "newpassword",
        }

        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password, payload["password"])
