# Generated by Django 2.2.13 on 2020-07-17 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("licences", "0016_auto_20200717_0952"),
    ]

    operations = [
        migrations.AlterField(
            model_name="licence",
            name="status",
            field=models.CharField(
                choices=[
                    ("issued", "Issued"),
                    ("reinstated", "Reinstated"),
                    ("revoked", "Revoked"),
                    ("surrendered", "Surrendered"),
                    ("suspended", "Suspended"),
                    ("draft", "Draft"),
                    ("cancelled", "Cancelled"),
                ],
                default="draft",
                max_length=32,
            ),
        ),
    ]
