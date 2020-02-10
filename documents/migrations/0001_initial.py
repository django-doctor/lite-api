# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
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
                ("name", models.CharField(max_length=1000)),
                ("s3_key", models.CharField(default=None, max_length=1000)),
                ("size", models.IntegerField(blank=True, null=True)),
                ("virus_scanned_at", models.DateTimeField(blank=True, null=True)),
                ("safe", models.NullBooleanField()),
            ],
            options={"abstract": False,},
        ),
    ]
