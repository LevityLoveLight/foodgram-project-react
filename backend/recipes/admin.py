from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 0


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientsInline(admin.TabularInline):
    model = Ingredient


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountInline, )
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'is_favorited',
        'ingredients',
    )
    readonly_fields = ('is_favorited',)
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    @admin.display(description='В избранном')
    def is_favorited(self, obj):
        return obj.favorites.count()

    def ingredients(self, obj):
        return list(obj.ingredients.all())


class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


admin.site.register(Tag, AdminTag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(IngredientAmount, IngredientRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
