from django.contrib import admin

# from recipes.models import (Tag, Ingredient, Cart, Favorite, Recipe)


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):

#     list_display = ('id', 'name', 'units_of_measure')
#     search_fields = ('name', )
#     empty_value_display = '-пусто-'
#     list_filter = ('name',)


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):

#     list_display = ('name', 'color', 'slug')
#     search_fields = ('name', )
#     empty_value_display = '-пусто-'
#     list_filter = ('name',)


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):

#     list_display = ('user', 'recipe', 'id')
#     search_fields = ('user', )
#     empty_value_display = '-пусто-'
#     list_filter = ('user',)


# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):

#     list_display = ('user', 'recipe')
#     search_fields = ('user', )
#     empty_value_display = '-пусто-'
#     list_filter = ('user',)


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):

#     list_display = ('id', 'author', 'name', 'cooking_time')
#     search_fields = ('name', 'author', 'tag')
#     empty_value_display = '-пусто-'
#     list_filter = ('name', 'author', 'tag')
