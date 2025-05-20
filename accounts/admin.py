from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'phone', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'phone', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
