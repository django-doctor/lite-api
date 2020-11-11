# Generated by Django 2.2.16 on 2020-11-09 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0016_firearmgooddetails_serial_number"),
        ("applications", "0039_auto_20201104_1047"),
    ]

    operations = [
        migrations.AddField(
            model_name="goodonapplication",
            name="firearm_details",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="goods.FirearmGoodDetails",
            ),
        ),
    ]
