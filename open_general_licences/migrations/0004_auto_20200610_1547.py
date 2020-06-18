# Generated by Django 2.2.13 on 2020-06-10 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("open_general_licences", "0003_opengenerallicencecase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="opengenerallicencecase",
            name="open_general_licence",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cases",
                to="open_general_licences.OpenGeneralLicence",
            ),
        ),
        migrations.AlterField(
            model_name="opengenerallicencecase",
            name="site",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="open_general_licence_cases",
                to="organisations.Site",
            ),
        ),
    ]
