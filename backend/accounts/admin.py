from backend.accounts.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib import admin

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Extra Info'), {'fields': ('nickname', 'description',)}),
        (_('Location'), {'fields': ('locale', 'coordinates','address', 'city', 'radius')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'nickname',
                    'date_joined', 'updated_on', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('email', 'nickname',
                     'date_joined', 'first_name', 'last_name')
    ordering = ('email',)

# django.template.exceptions.TemplateDoesNotExist: gis/openlayers.html
# Add 'django.contrib.gis' to INSTALLED_APPS.

