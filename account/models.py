from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Department(models.Model):
    #FINANCE_TEAM
    #LEGAL_TEAM
    #SECURITY_TEAM
    #SECURITY_TECH_TEAM
    name = models.CharField(max_length=100, null=True)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
