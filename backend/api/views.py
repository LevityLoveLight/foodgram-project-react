from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import FoodgramPagination
from .permissions import AdminOrReadOnly, IsAdmin, UserPermission, IsAuthorOrReadOnly
from .serializer import UserSerializer, TagSerializer, RecipeReadSerializer, RecipeWriteSerializer, RecipeSerializer, IngredientSerializer
from recipes.models import Recipe, Tag, Ingredient, IngredientAmount, Cart, Favorite
from users.models import Follow, User


class TagViewSet(viewsets.ModelViewSet):
    quaryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = AllowAny
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    quaryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = AllowAny
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @staticmethod
    def __get_intersection_model(request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = RecipeSerializer(recipe, context={'request': request})
        if request.method == 'POST':
            model.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        model.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self.__get_intersection_model(request, pk, Favorite)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.__get_intersection_model(request, pk, Cart)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data['new_password']
        )
        self.request.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
