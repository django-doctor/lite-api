# Generated by Django 2.2.11 on 2020-05-05 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0006_auto_20200501_1129"),
    ]

    operations = [
        migrations.AddField(
            model_name="externallocation",
            name="location_type",
            field=models.CharField(
                blank=True,
                choices=[("land_based", "Land based"), ("sea_based", "Vessel (sea) based")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="externallocation",
            name="country",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="countries.Country"
            ),
        ),
    ]
