# Generated by Django 4.2 on 2024-03-03 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='inrests',
            new_name='interests',
        ),
    ]
