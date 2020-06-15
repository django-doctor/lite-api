# Generated by Django 2.2.13 on 2020-06-12 11:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("licences", "0005_auto_20200610_1227"),
        ("organisations", "0008_auto_20200601_0814"),
    ]

    operations = [
        migrations.CreateModel(
            name="OpenLicenceReturns",
            fields=[
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created_at"
                    ),
                ),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("returns_data", models.TextField()),
                ("year", models.PositiveSmallIntegerField()),
                ("licences", models.ManyToManyField(related_name="open_licence_returns", to="licences.Licence")),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organisations.Organisation"),
                ),
            ],
            options={"abstract": False,},
        ),
    ]