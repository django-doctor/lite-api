# Generated by Django 2.2.11 on 2020-03-18 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0002_auto_20200213_1121"),
    ]

    operations = [
        migrations.AddField(
            model_name="casestatus", name="workflow_sequence", field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(model_name="casestatus", name="priority", field=models.PositiveSmallIntegerField(),),
    ]