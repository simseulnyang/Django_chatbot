from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib import admin
from django.http.request import HttpRequest
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserProfileInline(admin.StackedInline):
    model = Profile




class UserAdmin(BaseUserAdmin):

    ordering = ('email',)

    list_display = ('id', 'email', 'nickname')
    list_display_links = ('email', 'nickname')
    list_filter = ('email', 'nickname')
    search_fields = ('email', 'nickname')

    fieldsets = (
        ('info', {'fields': ('email', 'password', 'nickname', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', )}),
    )

    inlines = [
        UserProfileInline,
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'nickname', 'password1', 'password2')
            }
        ),
    )

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return('email', 'date_joined', )
        else:
            return('date_joined', )
        

    
        

admin.site.register(User, UserAdmin)
admin.site.register(Profile)