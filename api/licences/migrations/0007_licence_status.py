# Generated by Django 2.2.13 on 2020-07-03 09:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("licences", "0006_licence_sent_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="licence",
            name="status",
            field=models.CharField(
                choices=[
                    ("issued", "Issued"),
                    ("reinstated", "Reinstated"),
                    ("revoked", "Revoked"),
                    ("surrendered", "Surrendered"),
                    ("draft", "Draft"),
                    ("cancelled", "Cancelled"),
                    ("refused", "Refused"),
                ],
                default="draft",
                max_length=32,
            ),
        ),
    ]
