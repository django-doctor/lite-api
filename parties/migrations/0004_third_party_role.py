# Generated by Django 2.2.8 on 2020-01-13 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parties", "0003_timestampable"),
    ]

    operations = [
        migrations.AddField(
            model_name="thirdparty",
            name="role",
            field=models.CharField(
                choices=[
                    ("intermediate_consignee", "Intermediate Consignee"),
                    ("additional_end_user", "Additional End User"),
                    ("agent", "Agent"),
                    ("submitter", "Authorised Submitter"),
                    ("consultant", "Consultant"),
                    ("contact", "Contact"),
                    ("exporter", "Exporter"),
                    ("other", "Other"),
                ],
                default="other",
                max_length=22,
            ),
        ),
        migrations.AlterField(
            model_name="thirdparty",
            name="sub_type",
            field=models.CharField(
                choices=[
                    ("government", "Government"),
                    ("commercial", "Commercial Organisation"),
                    ("individual", "Individual"),
                    ("other", "Other"),
                ],
                default="other",
                max_length=20,
            ),
        ),
    ]