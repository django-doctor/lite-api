# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cases", "0004_auto_20200211_1459"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeneratedCaseDocument",
            fields=[
                (
                    "casedocument_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cases.CaseDocument",
                    ),
                ),
                ("text", models.TextField(blank=True, default=True)),
            ],
            options={"abstract": False,},
            bases=("cases.casedocument",),
        ),
    ]