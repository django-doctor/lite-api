# Generated by Django 2.2.4 on 2019-10-30 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0002_goodcountrydecision"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="case_activity",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="cases.CaseActivity",),
        ),
    ]