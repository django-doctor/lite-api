# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("documents", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Good",
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
                ("description", models.TextField(max_length=280)),
                (
                    "is_good_controlled",
                    models.CharField(
                        choices=[("yes", "Yes"), ("no", "No"), ("unsure", "I don't know")],
                        default="unsure",
                        max_length=20,
                    ),
                ),
                ("control_code", models.CharField(blank=True, default="", max_length=20, null=True)),
                (
                    "is_pv_graded",
                    models.CharField(
                        choices=[("yes", "Yes"), ("no", "No"), ("grading_required", "Good needs to be graded")],
                        default="grading_required",
                        max_length=20,
                    ),
                ),
                ("part_number", models.CharField(blank=True, default="", max_length=255, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("submitted", "Submitted"),
                            ("query", "Goods Query"),
                            ("verified", "Verified"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                (
                    "missing_document_reason",
                    models.CharField(
                        choices=[
                            ("NO_DOCUMENT", "No document available"),
                            ("OFFICIAL_SENSITIVE", "Document is above OFFICIAL-SENSITIVE"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                ("comment", models.TextField(blank=True, default=None, max_length=2000, null=True)),
                ("grading_comment", models.TextField(blank=True, default=None, max_length=2000, null=True)),
                ("report_summary", models.TextField(blank=True, default=None, max_length=5000, null=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="PvGradingDetails",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    "grading",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("uk_unclassified", "UK unclassified"),
                            ("uk_official", "UK official"),
                            ("uk_official_sensitive", "UK official - sensitive"),
                            ("uk_secret", "UK secret"),
                            ("uk_top_secret", "UK top secret"),
                            ("nato_unclassified", "NATO unclassified"),
                            ("nato_confidential", "NATO confidential"),
                            ("nato_restricted", "NATO restricted"),
                            ("nato_secret", "NATO secret"),
                            ("occar_unclassified", "OCCAR unclassified"),
                            ("occar_confidential", "OCCAR confidential"),
                            ("occar_restricted", "OCCAR restricted"),
                            ("occar_secret", "OCCAR secret"),
                        ],
                        default=None,
                        max_length=30,
                        null=True,
                    ),
                ),
                ("custom_grading", models.TextField(blank=True, max_length=100, null=True)),
                ("prefix", models.CharField(blank=True, max_length=30, null=True)),
                ("suffix", models.CharField(blank=True, max_length=30, null=True)),
                ("issuing_authority", models.CharField(blank=True, max_length=100, null=True)),
                ("reference", models.CharField(blank=True, max_length=100, null=True)),
                ("date_of_issue", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="GoodDocument",
            fields=[
                (
                    "document_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="documents.Document",
                    ),
                ),
                ("description", models.TextField(blank=True, default=None, max_length=280, null=True)),
                ("good", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="goods.Good")),
            ],
            options={"abstract": False,},
            bases=("documents.document",),
        ),
    ]