# Generated by Django 2.2.3 on 2019-07-17 08:51

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("countries", "0002_auto_20190628_1252"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False,),),
                ("address_line_1", models.TextField(default=None)),
                ("address_line_2", models.TextField(blank=True, default=None, null=True),),
                ("region", models.TextField(default=None)),
                ("postcode", models.CharField(max_length=10)),
                ("city", models.TextField(default=None)),
                ("country", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="countries.Country",),),
            ],
        ),
    ]
