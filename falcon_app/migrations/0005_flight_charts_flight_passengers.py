# Generated by Django 4.2.1 on 2023-05-20 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('falcon_app', '0004_flight_charts_flight_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight_charts',
            name='flight_passengers',
            field=models.CharField(max_length=240, null=True),
        ),
    ]
