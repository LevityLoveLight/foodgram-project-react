from rest_framework import serializers

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
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

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