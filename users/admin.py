import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
            'avatar',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email','name', 'password1', 'password2','avatar')
            }
        ),
    )
    def image_tag(self,obj):
        if obj.avatar:
            if os.path.isfile(obj.avatar.path):
                return format_html('<img class="rounded-circle" src="{}" style="width: 50px; height:50px;" />'.format(obj.avatar.url))
            else:
                return format_html('<img class="rounded-circle" src="/media/avatars/avatar.png" style="width: 45px; height:45px;" />')
        else:
            return format_html('<img class="rounded-circle" src="/media/avatars/avatar.png" style="width: 45px; height:45px;" />')
    list_display = ('email', 'name', 'is_staff','image_tag', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email','name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('image_tag',)


admin.site.register(User, UserAdmin)