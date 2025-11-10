from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'user_type', 'id',
        'email', 'is_active', 'is_staff'
    )
    search_fields = (
        'username', 'email',
        'user_type', 'id'
    )
    ordering = ('id',)


admin.site.register(CustomUser, CustomUserAdmin)
