from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin
)



class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.username = username
        user.save(using=self.db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)


# Create your models here.
class User(AbstractUser, PermissionsMixin):
    objects = UserManager()

    REQUIRED_FIELDS = ['email']
