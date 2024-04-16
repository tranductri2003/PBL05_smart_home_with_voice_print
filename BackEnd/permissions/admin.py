from django.contrib import admin
from .models import Permission

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('member', 'appliance')
    search_fields = ('user__name', 'appliance__name')

admin.site.register(Permission, PermissionAdmin)