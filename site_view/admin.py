from django.contrib import admin
from .models import *
# Register your models here.


def set_status_true(modeladmin, request, queryset):
    queryset.update(status=True)


set_status_true.short_description = "Mark selected sliders as status=True"


def set_status_false(modeladmin, request, queryset):
    queryset.update(status=False)


set_status_false.short_description = "Mark selected sliders as status=False"


@admin.register(Slider)
class Admin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image', 'status')
    actions = [set_status_false, set_status_true]


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'priority', 'status')


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image')
