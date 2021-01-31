from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import User, Address, Email
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'username', 'is_staff', 'last_login', 'date_joined')
    fieldsets = (
        (_('authentication data'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('province', 'city', 'postal_code')
    list_filter = ('province', 'city')


def make_published(modeladmin, request, queryset):
    queryset.update(daft=False)

make_published.short_description = "Mark selected stories as published"

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('author', 'subject', 'created', 'updated', 'publish', 'draft')
    list_filter = ('publish', 'draft')
    actions = [make_published]
