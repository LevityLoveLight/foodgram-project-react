from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenCreateView, TokenDestroyView

from api.views import UserViewSet, TagViewSet, RecipeViewSet, IngredientViewSet, FollowListViewSet, FollowViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'users/subscriptions/',
        FollowListViewSet.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path(
        'auth/token/login/', 
        TokenCreateView.as_view(),
        name='token-create'
    ),
    path(
        'auth/token/logout/', 
        TokenDestroyView.as_view(),
        name='token-destroy'
    ),
]
