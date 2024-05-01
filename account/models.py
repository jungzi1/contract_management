from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


DEPARTMENTS = [
    ("NORMAL", "NORMAL_TEAM"),
    ("FINANCE", "FINANCE_TEAM"),
    ("LEGAL", "LEGAL_TEAM"),
    ("SECURITY", "SECURITY_TEAM"),
    ("SECURITY_TECH", "SECURITY_TECH_TEAM"),
    ("ETC", "ETC_TEAM"),
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=15, choices=DEPARTMENTS)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return str(self.name)