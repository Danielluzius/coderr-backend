from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_user', 'business_user', 'title', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'customer_user__username', 'business_user__username']
