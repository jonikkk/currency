# Generated by Django 4.2.7 on 2023-12-03 13:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("currency", "0002_rename_id_contactus_contact_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Source",
            fields=[
                ("source_id", models.AutoField(primary_key=True, serialize=False)),
                ("source_url", models.TextField(max_length=255)),
                ("source_name", models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name="rate",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]