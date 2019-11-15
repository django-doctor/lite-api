# Generated by Django 2.2.4 on 2019-09-05 09:56

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
            name="Queue",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False,),),
                ("name", models.TextField(default="Untitled Queue")),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="teams.Team"),),
            ],
            options={"ordering": ["name"],},
        ),
    ]
