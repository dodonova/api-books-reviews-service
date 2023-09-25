from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from reviews.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    list_editable = ('role',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('О пользователе', {'fields': ('first_name', 'last_name', 'bio')}),
    )


admin.site.register(User, UserAdmin)
