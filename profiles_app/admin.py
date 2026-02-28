from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    """
    list_display = ('username', 'user_id', 'email', 'type', 'created_at')
    search_fields = ('username', 'email', 'type')
    fields = (
        'user', 'username', 'first_name', 'last_name', 'file',
        'location', 'tel', 'description', 'working_hours',
        'type', 'email', 'created_at'
    )
