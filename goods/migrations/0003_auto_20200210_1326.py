# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("goods", "0002_gooddocument_organisation"),
        ("flags", "0001_initial"),
        ("organisations", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gooddocument",
            name="user",
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="users.ExporterUser"),
        ),
        migrations.AddField(
            model_name="good", name="flags", field=models.ManyToManyField(related_name="goods", to="flags.Flag"),
        ),
        migrations.AddField(
            model_name="good",
            name="organisation",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organisations.Organisation"),
        ),
        migrations.AddField(
            model_name="good",
            name="pv_grading_details",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="goods.PvGradingDetails",
            ),
        ),
    ]