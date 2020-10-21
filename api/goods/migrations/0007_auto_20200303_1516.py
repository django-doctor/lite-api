# Generated by Django 2.2.10 on 2020-03-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0006_auto_20200226_1218"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pvgradingdetails",
            name="grading",
            field=models.CharField(
                blank=True,
                choices=[
                    ("uk_unclassified", "UK UNCLASSIFIED"),
                    ("uk_official", "UK OFFICIAL"),
                    ("uk_official_sensitive", "UK OFFICIAL - SENSITIVE"),
                    ("uk_secret", "UK SECRET"),
                    ("uk_top_secret", "UK TOP SECRET"),
                    ("nato_unclassified", "NATO UNCLASSIFIED"),
                    ("nato_confidential", "NATO CONFIDENTIAL"),
                    ("nato_restricted", "NATO RESTRICTED"),
                    ("nato_secret", "NATO SECRET"),
                    ("occar_unclassified", "OCCAR UNCLASSIFIED"),
                    ("occar_confidential", "OCCAR CONFIDENTIAL"),
                    ("occar_restricted", "OCCAR RESTRICTED"),
                    ("occar_secret", "OCCAR SECRET"),
                ],
                default=None,
                max_length=30,
                null=True,
            ),
        ),
    ]