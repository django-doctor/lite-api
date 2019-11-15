# Generated by Django 2.2.3 on 2019-07-30 18:40

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CaseStatus",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False,),),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("submitted", "Submitted"),
                            ("more_information_required", "More information required"),
                            ("under_review", "Under review"),
                            ("under_final_review", "Under final review"),
                            ("resubmitted", "Resubmitted"),
                            ("withdrawn", "Withdrawn"),
                            ("approved", "Approved"),
                            ("declined", "Declined"),
                        ],
                        max_length=50,
                    ),
                ),
                ("priority", models.IntegerField(null=False, blank=False)),
            ],
        ),
    ]
