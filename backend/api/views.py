import datetime

from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, 
                                        IsAuthenticatedOrReadOnly,
                                        SAFE_METHODS)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .pagination import FoodgramPagination
from .serializers import (FollowSerializer, IngredientListSerializer, 
                          RecipeReadSerializer, RecipeWriteSerializer,
                          ShortRecipeSerializer, TagSerializer)
from users.models import User, Follow


class UsersViewSet(UserViewSet):
    """Вью сет для Пользователя"""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        follows = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        follow_to = get_object_or_404(User, id=id)
        subscription = Follow.objects.filter(user=user, following=follow_to)
        if request.method == 'POST' and user.username != follow_to.username:
            Follow.objects.get_or_create(user=user, following=follow_to)
            serializer = FollowSerializer(
                follow_to, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE' and subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(ReadOnlyModelViewSet):
    """Вью сет для Тега"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вью сет для Ингредиента"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    """Вью сет для Рецептов"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    pagination_class = FoodgramPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            ShoppingCart.objects.get_or_create(
                user=user,
                recipe=recipe,
            )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        to_buy = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        to_buy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__purchases__user=request.user
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
        main_list = ([
            f"{item}: {value['amount']}"
            f"({value['measurement_unit']})\n"
            for item, value in shopping_list.items()]
        )
        today = datetime.date.today()
        main_list.append(f'Foodgram:{today.day}-{today.month}-{today.year}')
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="ShopCart.txt"'
        return response

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            Favorite.objects.get_or_create(
                user=user,
                recipe=recipe,
            )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
