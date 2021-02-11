from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'create', 'update')
    search_fields = ('name', 'slug', 'parent')
    list_filter = ('create', 'update')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'create', 'update')
    search_fields = ('name', 'slug')
    list_filter = ('create', 'update')


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'created', 'updated')
    search_fields = ('product',)
    list_filter = ('created', 'updated')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'slug', 'created', 'updated')
    search_fields = ('name', 'slug', 'brand', 'category')
    list_filter = ('brand', 'category', 'created', 'updated')


@admin.register(ProductMeta)
class ProductMetaAdmin(admin.ModelAdmin):
    list_display = ('product', 'updated')
    search_fields = ('product', )
    list_filter = ('created', 'updated')


@admin.register(MobileMeta)
class MobileMetaAdmin(admin.ModelAdmin):
    list_display = ('product', 'updated')
    search_fields = ('product', )
    list_filter = ('created', 'updated')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'title', 'rate', 'publish', 'draft')
    search_fields = ('author', 'product', 'title')
    list_filter = ('created', 'updated', 'publish', 'draft')


@admin.register(LikeProduct)
class LikeProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'condition')
    search_fields = ('user', 'product')
    list_filter = ('condition',)
