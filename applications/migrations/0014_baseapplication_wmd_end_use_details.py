# Generated by Django 2.2.11 on 2020-03-12 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0013_auto_20200311_1124"),
    ]

    operations = [
        migrations.AddField(
            model_name="baseapplication",
            name="compliant_limitations_eu_ref",
            field=models.TextField(blank=True, default=None, max_length=2200, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="informed_wmd_ref",
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="is_compliant_limitations_eu",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="is_eu_military",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="is_informed_wmd",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="is_military_end_use_controls",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="is_suspected_wmd",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="military_end_use_controls_ref",
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="baseapplication",
            name="suspected_wmd_ref",
            field=models.TextField(blank=True, default=None, max_length=2200, null=True),
        ),
    ]
