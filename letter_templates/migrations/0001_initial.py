# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import sortedm2m.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("picklists", "0001_initial"),
        ("cases", "0001_initial"),
        ("letter_layouts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LetterTemplate",
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
                ("name", models.CharField(max_length=35, unique=True)),
                ("case_types", models.ManyToManyField(related_name="letter_templates", to="cases.CaseType")),
                (
                    "layout",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="letter_layouts.LetterLayout"),
                ),
                (
                    "letter_paragraphs",
                    sortedm2m.fields.SortedManyToManyField(help_text=None, to="picklists.PicklistItem"),
                ),
            ],
            options={"ordering": ["name"],},
        ),
    ]
