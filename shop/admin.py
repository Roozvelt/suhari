from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False
    extra = 0

admin.site.register(Product)
admin.site.register(CartItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'user', 'total_price')

    # Позволит изменять статус заказа
    fieldsets = (
        (None, {
            'fields': ('user', 'created_at', 'status', 'contact_phone', 'contact_address')
        }),
    )

admin.site.register(OrderItem)