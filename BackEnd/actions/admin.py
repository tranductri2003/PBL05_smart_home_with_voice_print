from django.contrib import admin
from .models import Action

class ActionAdmin(admin.ModelAdmin):
    list_display = ('action_id', 'user_id', 'appliance_id', 'action', 'status', 'created_at')
    list_filter = ('action', 'status')
    search_fields = ('user_id__user_name', 'appliance_id__name', 'action')
    readonly_fields = ('action_id', 'created_at')

admin.site.register(Action, ActionAdmin)
