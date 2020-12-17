from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display_links = ('user', 'name', 'slug', 'status', 'closed')
    search_fields = ('name', 'slug')

    class Meta:
        ordering = ('status', 'closed')


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'quantity')
    search_fields = ('shop', 'product')

    class Meta:
        ordering = ['-quantity', 'price']