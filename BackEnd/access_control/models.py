from django.db import models
from users.models import NewUser
from appliances.models import Appliance
from helper.models import TimeSetup
from django.utils import timezone

# Create your models here.
class DevicePermission(TimeSetup, models.Model):
    permission_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  # Provide a default value

    def __str__(self):
        return f"{self.user.full_name} can control {self.appliance.name}"

