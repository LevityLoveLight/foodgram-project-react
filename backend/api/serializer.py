from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe


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