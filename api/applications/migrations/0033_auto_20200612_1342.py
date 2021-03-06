# Generated by Django 2.2.13 on 2020-06-12 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "reduce_good_on_application_decimal_places"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goodonapplication",
            name="licenced_value",
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name="goodonapplication",
            name="value",
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=15, null=True),
        ),
    ]
