from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(
        'about', max_length=500, blank=True,
        default="Em là fan cứng ba Duy"
    )
    
    def __str__(self):
        return self.name

