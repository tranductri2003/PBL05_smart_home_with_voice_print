from django.contrib import admin
from .models import Appliance

class ApplianceAdmin(admin.ModelAdmin):
    list_display = ('appliance_id', 'name', 'status')
    list_filter = ('status',)
    search_fields = ('appliance_id', 'name')

admin.site.register(Appliance, ApplianceAdmin)