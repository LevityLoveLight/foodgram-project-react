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
from .permissions import AdminOrReadOnly, IsAdmin, UserPermission
from .serializer import UserSerializer
# from recipes.models import Recipe, Tag, Ingredient, IngredientAmount, Cart
from users.models import Follow, User


# class TagViewSet(viewsets.ModelViewSet):
#     quaryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permissions_class = AllowAny
#     pagination_class = None


# class IngredientViewSet(viewsets.ModelViewSet):
#     quaryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     permissions_class = AllowAny
#     pagination_class = None


# class RecipeViewSet(viewsets.ModelViewSet):
#     quaryset = Recipe.objects.all()
#     permissions_class = AdminOrReadOnly
#     pagination_class = FoodgramPagination

#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return RecipeSerializer
#         return AddRecipeSerializer    

#     @action(detail=False)
#     def download_shopping_cart(self, request):
#         ingredients = get_shopping_list(request.user)
#         html_template = render_to_string('recipes/template_for_pdf.html',
#                                          {'ingredients': ingredients})
#         html = HTML(string=html_template)
#         result = html.write_pdf()
#         response = HttpResponse(result, content_type='application/pdf;')
#         response['Content-Disposition'] = 'inline; filename=shopping_list.pdf'
#         response['Content-Transfer-Encoding'] = 'binary'
#         return response


# @api_view(['POST', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def creat_delete_recipe(request, pk, model):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     if request.method == 'POST':
#         try:
#             model.objects.create(user=request.user, recipe=recipe)
#             answer = ShortRecipeSerializer(recipe)
#             return Response(answer.data, status=status.HTTP_201_CREATED
#                             )
#         except IntegrityError as error:
#             error_message = get_error_message(error.__str__(),
#                                               model.__name__)
#             return Response({'errors': error_message},
#                             status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         if model.objects.filter(user=request.user, recipe=recipe).count() == 0:
#             return Response({'errors': 'рецепта отсутствует в списке'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         obj = model.objects.get(user=request.user, recipe=recipe)
#         obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
