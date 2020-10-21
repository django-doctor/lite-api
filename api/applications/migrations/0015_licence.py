# Generated by Django 2.2.11 on 2020-03-16 10:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0014_baseapplication_wmd_end_use_details"),
    ]

    operations = [
        migrations.RemoveField(model_name="baseapplication", name="licence_duration",),
        migrations.CreateModel(
            name="Licence",
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
                ("start_date", models.DateField()),
                ("duration", models.PositiveSmallIntegerField()),
                ("is_complete", models.BooleanField(default=False)),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="licence",
                        to="applications.BaseApplication",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]