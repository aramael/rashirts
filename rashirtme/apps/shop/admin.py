from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'purchase_time', 'shirt_count', 'order_pretty', )
    actions = ['send_pickup_email', ]

    def send_pickup_email(self, request, queryset):
        for item in queryset:
            item.send_pickup()
    send_pickup_email.short_description = 'Send Pickup Notice'


admin.site.register(Order, OrderAdmin)