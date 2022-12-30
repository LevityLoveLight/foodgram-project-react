from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(filters.FilterSet):
    """Фильтр ингредиента"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(filters.FilterSet):
    """Фильтр рецепта"""
    is_favorited = filters.BooleanFilter(
        method='get_favorite',
        label='favorite',
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart',
        label='shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(is_favorite__user=self.request.user)
        return queryset.exclude(
            is_favorite__user=self.request.user
        )

    def get_is_in_shopping_cart(self, queryset, name, value):
        return Recipe.objects.filter(
            purchases__user=self.request.user) if value else None
