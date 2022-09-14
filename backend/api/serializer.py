from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField

from users.models import User, Follow
# from recipes.models import Tag, Ingredient, Recipe


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = "__all__"


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = "__all__"


# class RecipeSerializer(serializers.ModelSerializer):
#     tag = TagSerializer(
#         many=True,
#         read_only=True
#     )
#     ingredient = IngredientSerializer(
#         read_only=True
#     )
#     image = Base64ImageField()

#     class Meta:
#         model = Recipe
#         field = "__all__"


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(user=user, author=obj).exists()
