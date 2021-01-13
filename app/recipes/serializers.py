from core.models import Ingredient, Recipe, Tag
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class TagSerializer(ModelSerializer):
    """
    Serializer for tag object
    """

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(ModelSerializer):
    """
    Serializer for ingredient objects
    """

    class Meta:
        model = Ingredient
        fields = ("id", "name")
        ready_only_fields = ("id",)


class RecipeSerializer(ModelSerializer):
    """
    Serialize a recipe
    """

    ingredients = PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
    )
    tags = PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "ingredients",
            "tags",
            "time_minutes",
            "price",
            "link",
        )
        read_only_fields = ("id",)
