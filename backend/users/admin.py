from django.contrib import admin

from users.models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'login', 'id')
    search_fields = ('login', 'email')
    empty_value_display = '-пусто-'
    list_filter = ('email', 'login')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')
    search_fields = ('user',)
    empty_value_display = "-пусто-"
    list_filter = ('user',)
