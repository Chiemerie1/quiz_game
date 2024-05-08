from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from  django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUsermanager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user.set_password(password)



class User(AbstractUser)