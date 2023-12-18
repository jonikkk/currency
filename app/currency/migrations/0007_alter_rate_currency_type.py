# Generated by Django 4.2.7 on 2023-12-11 12:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("currency", "0006_alter_contactus_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rate",
            name="currency_type",
            field=models.SmallIntegerField(
                choices=[("1", "Dollar"), ("2", "Euro")], default="1"
            ),
        ),
    ]