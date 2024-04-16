from django.db import models
from members.models import Member
from appliances.models import Appliance

# Create your models here.
class Permission(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.name} can control {self.appliance.name}"
