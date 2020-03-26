# Generated by Django 2.2.11 on 2020-03-24 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0017_auto_20200320_1109"),
    ]

    operations = [
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="electronic_warfare_requirement",
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication", name="expedited", field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="expedited_date",
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="foreign_technology",
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="foreign_technology_description",
            field=models.CharField(max_length=2200, null=True),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="locally_manufactured",
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="locally_manufactured_description",
            field=models.CharField(max_length=2200, null=True),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="mtcr_type",
            field=models.CharField(
                choices=[
                    ("mtcr_category_1", "MTCR Category 1"),
                    ("mtcr_category_2", "MTCR Category 2"),
                    ("none", "No"),
                    ("unknown", "Unknown"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="prospect_value",
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="uk_service_equipment",
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="uk_service_equipment_description",
            field=models.CharField(max_length=2200, null=True),
        ),
        migrations.AddField(
            model_name="f680clearanceapplication",
            name="uk_service_equipment_type",
            field=models.CharField(
                choices=[
                    ("mod_funded", "MOD funded"),
                    ("part_mod_part_venture", "Part MOD part private venture"),
                    ("private_venture", "Private venture"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]