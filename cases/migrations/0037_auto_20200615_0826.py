# Generated by Django 2.2.13 on 2020-06-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0036_case_additional_contacts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="additional_contacts",
            field=models.ManyToManyField(related_name="case", to="parties.Party"),
        ),
    ]