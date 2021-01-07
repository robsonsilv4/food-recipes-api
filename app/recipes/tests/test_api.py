from core.models import Tag
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import TagSerializer

TAGS_URL = reverse("recipes:tag-list")


class PublicAPITest(TestCase):
    """
    Test the public avaliable Tags API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login is required for retrieving tags
        """
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITest(TestCase):
    """
    Test the authorized user Tags API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test retrieving tags
        """
        Tag.objects.create(user=self.user, name="Test")
        Tag.objects.create(user=self.user, name="Tag")

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test that tags returned are for the authenticated user
        """
        another_user = get_user_model().objects.create_user(
            "another@test.com",
            "anotherpassword",
        )
        Tag.objects.create(user=another_user, name="Another")
        tag = Tag.objects.create(user=self.user, name="More")

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], tag.name)
