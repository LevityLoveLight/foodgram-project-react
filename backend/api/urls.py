from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (TagViewSet, RecipeViewSet, IngredientViewSet,
                       UserViewSet, get_jwt_token, signup)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', signup),
    path('auth/token/', get_jwt_token),
]
