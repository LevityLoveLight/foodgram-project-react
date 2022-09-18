from rest_framework.generics import ListAPIView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        SAFE_METHODS)
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .utils import make_shopping_list
from .pagination import FoodgramPagination
from .permissions import UserPermission, IsAuthorOrReadOnly
from .serializer import UserSerializer, TagSerializer, RecipeReadSerializer, RecipeWriteSerializer, RecipeSerializer, IngredientSerializer, FavoriteSerializer, FollowSerializer, CartSerializer
from recipes.models import Recipe, Tag, Ingredient, IngredientAmount, Cart, Favorite
from users.models import Follow, User


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @staticmethod
    def create_object(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_object(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        object = get_object_or_404(model, user=user, recipe=recipe)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticatedOrReadOnly,),
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.create_object(
                request=request,
                pk=pk,
                serializers=FavoriteSerializer,
            )
        return self.delete_object(request=request, pk=pk, model=Favorite)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticatedOrReadOnly,),
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.create_object(
                request=request,
                pk=pk,
                serializers=CartSerializer,
            )
        return self.delete_object(request=request, pk=pk, model=Cart)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticatedOrReadOnly,),
    )
    def download_shopping_cart(self, user):
        main_list = make_shopping_list(user)
        filename = 'shopping-list.txt'
        response = HttpResponse(main_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response


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


class FollowListViewSet(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class FollowViewSet(APIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(
                user=request.user,
                author_id=user_id,
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на данного автора.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Follow.objects.create(
            user=request.user,
            author_id=user_id,
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        following = Follow.objects.filter(
            user=request.user,
            author_id=user_id,
        )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
