# Generated by Django 2.2.17 on 2021-01-15 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("external_data", "0004_denial_is_revoked_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="denial",
            name="reference",
            field=models.TextField(
                help_text="The reference code assigned by the authority that created the denial", unique=True
            ),
        ),
    ]
