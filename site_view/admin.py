from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Slider)
class Admin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image')


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'priority', 'status')



@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image')

