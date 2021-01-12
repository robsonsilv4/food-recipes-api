from core.models import Ingredient, Tag
from rest_framework.serializers import ModelSerializer


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
