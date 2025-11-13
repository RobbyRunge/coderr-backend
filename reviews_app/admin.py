from django.contrib import admin

from .models import Review  # Importiere dein Modell


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'description', 'rating',
        'business_user', 'reviewer', 'created_at',
        'updated_at'
    )
    search_fields = ('description',)
    list_filter = ('rating',)
