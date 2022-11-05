from django import forms
from django.forms import ModelForm
from core.models import User, Projects


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'
