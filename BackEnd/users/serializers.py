from rest_framework import serializers
from .models import NewUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id', 'user_name', 'full_name', 'about', 'phone_number', 'date_of_birth', 'role', 'is_staff', 'is_active']

