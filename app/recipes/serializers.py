from core.models import Tag
from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):
    """
    Serializer for tag object
    """

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)
