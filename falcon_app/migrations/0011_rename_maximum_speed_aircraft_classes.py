# Generated by Django 4.2.1 on 2023-05-22 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('falcon_app', '0010_aircraft'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aircraft',
            old_name='maximum_speed',
            new_name='classes',
        ),
    ]
