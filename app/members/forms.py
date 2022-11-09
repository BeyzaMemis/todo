from django import forms
from django.forms import ModelForm
from core.models import User, Projects


class UserForm(ModelForm):


    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),


        }


class UserUpdateForm(ModelForm):
    current_project = forms.ModelChoiceField(queryset=Projects.objects.all(), empty_label=None)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active', 'date_joined',
                  'total_worked_project', 'active_work_project_count', 'current_project']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'current_project': forms.Select(attrs={'class': 'custom-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_joined': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'total_worked_project': forms.NumberInput(attrs={'class': 'form-control'}),
            'active_work_project_count': forms.NumberInput(attrs={'class': 'form-control'})

        }


class ProjectForm(ModelForm):
    path = forms.CharField(required=False)

    class Meta:
        model = Projects
        fields = '__all__'
