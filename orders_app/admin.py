from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'id', 'status', 'created_at')
    search_fields = ('customer_user__username', 'status')
    list_filter = ('status', 'created_at')

    def get_customer_name(self, obj):
        return obj.customer_user.username
    get_customer_name.short_description = 'Customer Name'