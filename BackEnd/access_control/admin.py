from django.contrib import admin
from .models import DevicePermission

class DevicePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'appliance')
    search_fields = ('user__user_name', 'appliance__name')

admin.site.register(DevicePermission, DevicePermissionAdmin)
