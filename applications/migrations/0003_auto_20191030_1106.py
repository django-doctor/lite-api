# Generated by Django 2.2.4 on 2019-10-30 11:06
import django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0002_applicationdocument"),
    ]

    operations = [
        migrations.AlterField(
            model_name="baseapplication",
            name="licence_type",
            field=models.CharField(
                choices=[
                    ("standard_licence", "Standard Licence"),
                    ("open_licence", "Open Licence"),
                    ("hmrc_query", "HMRC Query"),
                ],
                default=None,
                max_length=50,
            ),
        ),
        migrations.RenameField(model_name="baseapplication", old_name="licence_type", new_name="application_type",),
        migrations.CreateModel(
            name="HmrcQuery",
            fields=[
                (
                    "baseapplication_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="applications.BaseApplication",
                    ),
                ),
                (
                    "consignee",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hmrc_query_consignee",
                        to="parties.Consignee",
                    ),
                ),
                (
                    "end_user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hmrc_query_end_user",
                        to="parties.EndUser",
                    ),
                ),
                (
                    "third_parties",
                    models.ManyToManyField(related_name="hmrc_query_third_parties", to="parties.ThirdParty"),
                ),
                (
                    "ultimate_end_users",
                    models.ManyToManyField(related_name="hmrc_query_ultimate_end_users", to="parties.UltimateEndUser",),
                ),
            ],
            bases=("applications.baseapplication",),
        ),
    ]
