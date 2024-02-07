from django.db import models
from users.models import NewUser
from appliances.models import Appliance
from helper.models import TimeSetup

ACTION_CHOICES = (
    ('ON', 'Bật'),
    ('OFF', 'Tắt'),
    ('VIEW', 'Xem trạng thái'),
)

# Create your models here.
class Action(TimeSetup, models.Model):
    action_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    appliance_id = models.ForeignKey(Appliance, on_delete=models.CASCADE)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Action ID: {self.action_id}, User: {self.user_id}, Appliance: {self.appliance_id}, Action: {self.action}, Status: {self.status}"
    
