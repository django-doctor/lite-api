# Generated by Django 2.2.8 on 2019-12-11 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flags", "0001_initial"),
        ("countries", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="country", name="flags", field=models.ManyToManyField(related_name="countries", to="flags.Flag"),
        ),
    ]