# Generated by Django 2.2.8 on 2019-12-24 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
        ("cases", "0003_auto_20191209_1209"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="case_officer",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="users.GovUser"),
        ),
    ]