# Generated by Django 5.0.1 on 2024-01-31 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_remove_community_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='c_image',
            field=models.FileField(upload_to='community_image'),
        ),
    ]
