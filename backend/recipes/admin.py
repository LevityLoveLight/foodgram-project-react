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


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'amount',
    )
    list_filter = ('ingredient',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'tags__name', 'favorites',)
    search_fields = ('name', 'author__username', 'tags__name')
    list_filter = ('tags',)
    empty_value_display = '-пусто-'
    inlines = (
        IngredientAmountInline,
    )

    def favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


admin.site.register(Tag, AdminTag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientInRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
