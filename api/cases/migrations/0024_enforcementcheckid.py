# Generated by Django 2.2.12 on 2020-05-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0023_auto_20200515_1248"),
    ]

    operations = [
        migrations.CreateModel(
            name="EnforcementCheckID",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("entity_id", models.UUIDField(unique=True)),
            ],
        ),
    ]