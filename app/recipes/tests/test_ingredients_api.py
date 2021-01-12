from core.models import Ingredient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipes:ingredient-list")


class PublicIngredientsAPITest(TestCase):
    """Test the publicity avaliable ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITest(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """
        Test retrieving a list of ingredients
        """
        Ingredient.objects.create(user=self.user, name="Test")
        Ingredient.objects.create(user=self.user, name="Again")

        response = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returnded"""
        another_user = get_user_model().objects.create_user(
            "another@test.com",
            "anotherpassword",
        )

        Ingredient.objects.create(user=another_user, name="Another")
        ingredient = Ingredient.objects.create(user=self.user, name="Name")
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], ingredient.name)
