# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExternalLocation",
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
                ("name", models.TextField(default=None)),
                ("address", models.TextField(default=None)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Organisation",
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
                ("name", models.TextField(blank=True, default=None)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("hmrc", "HMRC"),
                            ("commercial", "Commercial Organisation"),
                            ("individual", "Individual"),
                        ],
                        default="commercial",
                        max_length=20,
                    ),
                ),
                ("eori_number", models.TextField(blank=True, default=None, null=True)),
                ("sic_number", models.TextField(blank=True, default=None, null=True)),
                ("vat_number", models.TextField(blank=True, default=None, null=True)),
                ("registration_number", models.TextField(blank=True, default=None, null=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Site",
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
                ("name", models.TextField(default=None)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="site", to="addresses.Address"
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="site",
                        to="organisations.Organisation",
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
    ]
