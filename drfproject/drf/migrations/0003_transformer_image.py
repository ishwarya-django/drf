# Generated by Django 4.1 on 2022-11-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drf', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='transformer',
            name='image',
            field=models.ImageField(default=2, upload_to=''),
            preserve_default=False,
        ),
    ]
