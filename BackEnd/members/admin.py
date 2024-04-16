from django.contrib import admin
from .models import Member

class ApplianceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'about')
    list_filter = ('name',) 
    search_fields = ('name', 'about')

admin.site.register(Member, ApplianceAdmin)