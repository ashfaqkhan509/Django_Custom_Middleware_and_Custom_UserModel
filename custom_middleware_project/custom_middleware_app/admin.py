from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Update User Admin view in 4 parts
        - Username, password,
        - first_name, last_name
        - is_active, is_staff, is_superuser
        - last login
    """
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'role')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'role')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        ('Login Credentials', {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login',)
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
