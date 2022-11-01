from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    USERNAME_FIELD = 'email'

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user


# Create your models here.
class User(AbstractUser, PermissionsMixin):
    objects = UserManager()

    REQUIRED_FIELDS = ['email']

