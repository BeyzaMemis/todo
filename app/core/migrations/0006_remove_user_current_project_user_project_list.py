# Generated by Django 4.1.2 on 2022-11-11 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprojectrelation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='current_project',
        ),
        migrations.AddField(
            model_name='user',
            name='project_list',
            field=models.TextField(null=True),
        ),
    ]
