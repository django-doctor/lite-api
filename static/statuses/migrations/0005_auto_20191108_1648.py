# Generated by Django 2.2.4 on 2019-11-08 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0004_auto_20191107_1424"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casestatus",
            name="priority",
            field=models.IntegerField(
                choices=[
                    ("submitted", 1),
                    ("applicant_editing", 2),
                    ("resubmitted", 3),
                    ("initial_checks", 4),
                    ("under_review", 5),
                    ("under_final_review", 6),
                    ("finalised", 7),
                    ("withdrawn", 8),
                ]
            ),
        ),
    ]