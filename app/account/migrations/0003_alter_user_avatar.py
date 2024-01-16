# Generated by Django 4.2.7 on 2024-01-04 14:27

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_alter_user_options_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.FileField(
                blank=True,
                default=None,
                null=True,
                upload_to=account.models.user_directory_path,
                verbose_name="Avatar",
            ),
        ),
    ]
