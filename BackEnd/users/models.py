from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from helper.models import TimeSetup


ROLES = [
    ("A", "Admin"),
    ("N", "Normal"),
]



class CustomAccountManager(BaseUserManager):
    def create_superuser(self, user_name, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(user_name, full_name, password, **extra_fields)


    def create_user(self, user_name, full_name, password, **other_fields):
        if not user_name:
            raise ValueError(_('The user_name field must be set.'))
        
        user = self.model(user_name=user_name, full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user




class NewUser(TimeSetup, AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50)

    about = models.TextField(_(
        'about'), max_length=500, blank=True, default="Em là sinh viên Bách Khoa")
    
    phone_number = models.CharField(max_length=100)
    date_of_birth = models.DateField(auto_now_add=True)
    role = models.CharField(choices=ROLES, default="N", max_length=1)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['full_name']
    
    objects = CustomAccountManager()

    def __str__(self):
        return self.full_name