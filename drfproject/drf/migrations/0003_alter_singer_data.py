# Generated by Django 5.0.6 on 2024-05-21 05:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drf', '0002_singer_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singer',
            name='data',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Invalid data format', regex='^[A-Za-z][a-zA-Z]*$')]),
        ),
    ]
