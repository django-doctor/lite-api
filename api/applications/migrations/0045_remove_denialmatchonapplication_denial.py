# Generated by Django 2.2.16 on 2021-01-13 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("external_data", "0003_auto_20210112_1059"),
        ("applications", "0044_denialmatchonapplication"),
    ]

    operations = [
        migrations.RemoveField(model_name="denialmatchonapplication", name="denial",),
        migrations.AddField(
            model_name="denialmatchonapplication",
            name="denial",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="denial_matches_on_application",
                to="external_data.Denial",
            ),
            preserve_default=False,
        ),
    ]