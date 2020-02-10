# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Audit",
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
                ("actor_object_id", models.CharField(db_index=True, max_length=255)),
                ("verb", models.CharField(db_index=True, max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("target_object_id", models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ("action_object_object_id", models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ("payload", jsonfield.fields.JSONField(default=dict)),
                (
                    "action_object_content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="action_object",
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "actor_content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="actor",
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "target_content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="target",
                        to="contenttypes.ContentType",
                    ),
                ),
            ],
            options={"ordering": ("-created_at",),},
        ),
    ]
