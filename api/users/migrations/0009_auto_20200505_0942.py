# Generated by Django 2.2.11 on 2020-05-05 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_auto_20200501_1329"),
    ]

    operations = [
        migrations.AlterField(
            model_name="govuser",
            name="team",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="users", to="teams.Team"),
        ),
    ]
