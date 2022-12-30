from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


class UserAdmin(UserAdmin):
    model = User
    list_display = (
        'id', 
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'password', 
        'is_staff', 
        'is_active'
    )
    ordering = ('email', )
    search_fields = ('username', 'email', )
    ordering = ('email', )


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
