from core.models import Ingredient, Tag
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .serializers import IngredientSerializer, TagSerializer


class TagViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """
    Manage tags in the database
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Return objects for the current authenticated user only
        """
        return self.queryset.filter(
            user=self.request.user,
        ).order_by("-name")

    def perform_create(self, serializer):
        """
        Create a new tag
        """
        serializer.save(user=self.request.user)


class IngredientViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """
    Manage ingredients in the database
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """
        Return objects for the current authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """
        Create a new ingredient
        """
        serializer.save(user=self.request.user)
