# Generated by Django 2.2.9 on 2020-01-24 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team", name="name", field=models.CharField(default=None, max_length=60, unique=True),
        ),
    ]