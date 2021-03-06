# Generated by Django 2.2.10 on 2020-03-10 10:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0001_initial"),
        ("flags", "0002_auto_20200227_1130"),
    ]

    operations = [
        migrations.CreateModel(
            name="FlaggingRule",
            fields=[
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created_at"
                    ),
                ),
                (
                    "updated_at",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="updated_at"
                    ),
                ),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
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
                        choices=[("Active", "Active"), ("Deactivated", "Deactivated")], default="Active", max_length=20
                    ),
                ),
                ("matching_value", models.CharField(max_length=100)),
                ("flag", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="flags.Flag")),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="teams.Team")),
            ],
            options={"abstract": False,},
        ),
    ]
