# Generated by Django 2.2.8 on 2019-12-16 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("queries", "0001_initial"),
        ("parties", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EndUserAdvisoryQuery",
            fields=[
                (
                    "query_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="queries.Query",
                    ),
                ),
                ("note", models.TextField(blank=True, default=None, null=True)),
                ("reasoning", models.TextField(blank=True, default=None, null=True)),
                ("nature_of_business", models.TextField(blank=True, default=None, null=True)),
                ("contact_name", models.TextField(blank=True, default=None, null=True)),
                ("contact_email", models.EmailField(blank=True, default=None, max_length=254)),
                ("contact_job_title", models.TextField(blank=True, default=None, null=True)),
                ("contact_telephone", models.CharField(default=None, max_length=15)),
                (
                    "copy_of",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="end_user_advisories.EndUserAdvisoryQuery",
                    ),
                ),
                (
                    "end_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, related_name="eua_query", to="parties.EndUser"
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("queries.query",),
        ),
    ]
