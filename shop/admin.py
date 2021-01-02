from django.contrib import admin
from .models import BasketItem, Basket, Shop, ShopProduct, Order, OrderItem, Payment


# Register your models here.
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slug', 'status', 'closed')
    search_fields = ('name', 'slug')
    list_filter = ('joined', 'status', 'closed')

    class Meta:
        ordering = ('status', 'closed')


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'quantity')
    search_fields = ('shop', 'product')
    list_filter = ('shop', 'product', 'created', 'updated')

    class Meta:
        ordering = ['-quantity', 'price']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'shop_product', 'count', 'price', 'create_at', 'update_at')
    search_fields = ('shop_product', 'order')
    list_filter = ('count', )

    class Meta:
        ordering = ['-create_at', '-update_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'create_at', 'update_at', 'paid')
    search_fields = ('user', )
    list_filter = ('paid',)

    class Meta:
        ordering = ['-paid', '-create_at', '-update_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'paid_price', 'create_at', 'update_at')
    search_fields = ('user', 'order')


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'shop_product', 'count', 'create_at', 'update_at')
    search_fields = ('baset', 'shop_product')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'create_at', 'update_at')
    search_fields = ('user', )

