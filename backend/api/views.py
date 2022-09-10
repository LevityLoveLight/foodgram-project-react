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
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import FoodgramPagination
from .permissions import AdminOrReadOnly, IsAdmin
from .serializer import TagSerializer, IngredientSerializer, RecipeSerializer, UserCreateSerializer, UserTokenSerializer, UserSerializer
from recipes.models import Recipe, Tag, Ingredient, IngredientAmount, Cart
from users.models import Follow, User


class TagViewSet(viewsets.ModelViewSet):
    quaryset = Tag.objects.all()
    serializer_class = TagSerializer
    permissions_class = AllowAny
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    quaryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permissions_class = AllowAny
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    quaryset = Recipe.objects.all()
    permissions_class = AdminOrReadOnly
    pagination_class = FoodgramPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return AddRecipeSerializer    

    @action(detail=False)
    def download_shopping_cart(self, request):
        ingredients = get_shopping_list(request.user)
        html_template = render_to_string('recipes/template_for_pdf.html',
                                         {'ingredients': ingredients})
        html = HTML(string=html_template)
        result = html.write_pdf()
        response = HttpResponse(result, content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=shopping_list.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        return response


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def creat_delete_recipe(request, pk, model):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        try:
            model.objects.create(user=request.user, recipe=recipe)
            answer = ShortRecipeSerializer(recipe)
            return Response(answer.data, status=status.HTTP_201_CREATED
                            )
        except IntegrityError as error:
            error_message = get_error_message(error.__str__(),
                                              model.__name__)
            return Response({'errors': error_message},
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if model.objects.filter(user=request.user, recipe=recipe).count() == 0:
            return Response({'errors': 'рецепта отсутствует в списке'},
                            status=status.HTTP_400_BAD_REQUEST)
        obj = model.objects.get(user=request.user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = FoodgramPagination
    lookup_field = 'username'

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    default_token_generator.check_token(user, confirmation_code)
    refresh = RefreshToken.for_user(user)
    return Response({
        'token': (refresh.access_token)},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    user, _ = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        "Foodgram account activation",
        "confirmation_code: " + confirmation_code,
        "admin@foodgram.com",
        [email],
        fail_silently=False,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )