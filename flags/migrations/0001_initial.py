# Generated by Django 2.2.3 on 2019-07-17 08:51

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Flag",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False,),),
                ("name", models.TextField(default="Untitled Flag")),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("Case", "Case"),
                            ("Organisation", "Organisation"),
                            ("Good", "Good"),
                            ("Destination", "Destination"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Deactivated", "Deactivated")], default="Active", max_length=20,
                    ),
                ),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="teams.Team"),),
            ],
        ),
    ]
