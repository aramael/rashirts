from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'purchase_time', 'shirt_count', 'order_pretty', )

admin.site.register(Order, OrderAdmin)