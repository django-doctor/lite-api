# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DenialReason",
            fields=[
                ("id", models.CharField(editable=False, max_length=3, primary_key=True, serialize=False)),
                ("deprecated", models.BooleanField(default=False)),
            ],
        ),
    ]
