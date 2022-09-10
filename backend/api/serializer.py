from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from recipes.models import Tag, Ingredient, Recipe
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(
        many=True,
        read_only=True
    )
    ingredient = IngredientSerializer(
        read_only=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        field = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    login = serializers.CharField(required=True)

    def validate(self, data):
        email = data['email']
        username = data['username']
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'Уже зарегестрирован'})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'Уже зарегестрирован'})
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
