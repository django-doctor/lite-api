# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("countries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("address_line_1", models.TextField(default=None)),
                ("address_line_2", models.TextField(blank=True, default=None, null=True)),
                ("region", models.TextField(default=None)),
                ("postcode", models.CharField(max_length=10)),
                ("city", models.TextField(default=None)),
                ("country", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="countries.Country")),
            ],
        ),
    ]
