from django import forms
from django.forms import ModelForm
from core.models import User, Projects


class UserForm(ModelForm):
    current_project = forms.ModelChoiceField(queryset=Projects.objects.all(), empty_label=None)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'current_project']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'current_project': forms.Select(attrs={'class': 'custom-control'}),

        }



class ProjectForm(ModelForm):
    path = forms.CharField(required=False)

    class Meta:
        model = Projects
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'active_issue_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'solved_issue_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'start_date': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'deadline': forms.SelectDateWidget(attrs={'class': 'form-control'})
        }
