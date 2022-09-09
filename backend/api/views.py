from django.shortcuts import render
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny

from .pagination import FoodgramPagination
from .permissions import AdminOrReadOnly
from .serializer import TagSerializer, IngredientSerializer, RecipeSerializer
from recipes.models import Recipe, Tag, Ingredient, IngredientAmount, Cart
from users.models import Follow, User


class UserCreatView(UserViewSet):
    serializer_class = 
    queryset = User.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    quaryset = Tag.objects.all()
    serializer_class = TagSerializer
    permissions_class = AllowAny
    pegination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    quaryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permissions_class = AllowAny
    pegination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    quaryset = Recipe.objects.all()
    serializer_class = TagSerializer
    permissions_class = AdminOrReadOnly
    pegination_class = FoodgramPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
