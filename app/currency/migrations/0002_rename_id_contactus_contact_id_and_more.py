# Generated by Django 4.2.7 on 2023-11-16 16:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("currency", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactus",
            old_name="id",
            new_name="contact_id",
        ),
        migrations.RenameField(
            model_name="rate",
            old_name="type",
            new_name="currency_type",
        ),
    ]