# Generated by Django 2.2.11 on 2020-03-07 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0003_organisation_status"),
    ]

    operations = [
        migrations.AlterModelOptions(name="organisation", options={"ordering": ["name"]},),
        migrations.AlterField(
            model_name="organisation",
            name="status",
            field=models.CharField(
                choices=[("active", "Active"), ("in_review", "In review")], default="in_review", max_length=20
            ),
        ),
    ]