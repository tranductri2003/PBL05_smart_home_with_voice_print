from django.db import models
from helper.models import TimeSetup

# Create your models here.
class Appliance(TimeSetup, models.Model):
    appliance_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    humidity = models.FloatField(default=0)
    temparature = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    