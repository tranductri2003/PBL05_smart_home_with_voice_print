from rest_framework import serializers
from .models import Appliance

class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ['appliance_id', 'name', 'description', 'status', 'humidity', 'temparature']
