import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import TextInput, Textarea, CharField
from users.models import NewUser

class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('user_name', 'full_name',)
    list_filter = ('user_name', 'full_name', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('user_name', 'full_name', 'role', 'is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('user_name', 'full_name')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'groups')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.CharField: {'widget': TextInput(attrs={'size': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'full_name', 'phone_number', 'role','is_active', 'is_staff')}
        ),
    )



admin.site.register(NewUser, UserAdminConfig)