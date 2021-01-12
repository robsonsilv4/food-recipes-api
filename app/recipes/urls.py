from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet

router = DefaultRouter()
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)

app_name = "recipes"

urlpatterns = [
    path("", include(router.urls)),
]
