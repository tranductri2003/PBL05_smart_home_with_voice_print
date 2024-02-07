from rest_framework import serializers
from .models import DevicePermission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevicePermission
        fields = ['permission_id', 'user', 'appliance', 'created_at']
