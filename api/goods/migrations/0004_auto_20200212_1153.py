# Generated by Django 2.2.10 on 2020-02-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0003_auto_20200210_1326"),
    ]

    operations = [
        migrations.AlterField(
            model_name="good",
            name="missing_document_reason",
            field=models.CharField(
                choices=[
                    ("NO_DOCUMENT", "No document available for the product"),
                    ("OFFICIAL_SENSITIVE", "Document is above official-sensitive"),
                ],
                max_length=30,
                null=True,
            ),
        ),
    ]