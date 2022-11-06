from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=257, unique=True, null=False)
    description = models.TextField()
    active_issue_count = models.IntegerField(default=0)  # functiona bağlanmalı
    solved_issue_count = models.IntegerField(default=0)  # functiona bağlanmalı
    is_active = models.BooleanField()
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()




class Projects(models.Model):
    name = models.CharField(max_length=257, unique=True, null=False)
    description = models.TextField()
    active_issue_count = models.IntegerField(default=0,null=True)  # functiona bağlanmalı
    solved_issue_count = models.IntegerField(default=0, null=True)  # functiona bağlanmalı
    is_active = models.BooleanField()
    start_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, project=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.username = username
        user.current_project = project
        user.save(using=self.db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


# Create your models here.
class User(AbstractUser, PermissionsMixin):
    objects = UserManager()
    related_group = models.CharField
    current_project = models.ForeignKey(to='core.Projects', related_name='current_project', on_delete=models.PROTECT, null=True)
    total_worked_project = models.IntegerField(default=0)  # functiona bağla
    active_work_project_count = models.IntegerField(default=0)  # functiona bağla

    REQUIRED_FIELDS = ['email']
