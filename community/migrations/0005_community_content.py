# Generated by Django 5.0.1 on 2024-01-31 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_rename_c_image_community_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
