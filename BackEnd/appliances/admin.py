from django.contrib import admin
from .models import Appliance

class ApplianceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_filter = ('name',) 
    search_fields = ('name', 'description')

admin.site.register(Appliance, ApplianceAdmin)