from core.models import Ingredient, Tag
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .serializers import IngredientSerializer, TagSerializer


class BaseViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """
    Base viewset for user owned recipe attributes
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return objects for the current authenticated user only
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """
        Create a new object
        """
        serializer.save(user=self.request.user)


class TagViewSet(BaseViewSet):
    """
    Manage tags in the database
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseViewSet):
    """
    Manage ingredients in the database
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
