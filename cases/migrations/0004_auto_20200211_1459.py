# Generated by Django 2.2.10 on 2020-02-11 14:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0003_auto_20200210_1326"),
    ]

    operations = [
        migrations.RemoveField(model_name="case", name="type",),
        migrations.RemoveField(model_name="casetype", name="id",),
        migrations.RemoveField(model_name="casetype", name="name",),
        migrations.AddField(
            model_name="casetype",
            name="reference",
            field=models.CharField(
                choices=[
                    ("oiel", "Open Individual Export Licence"),
                    ("ogel", "Open General Export Licence"),
                    ("oicl", "Open Individual Trade Control Licence"),
                    ("siel", "Standard Individual Export Licence"),
                    ("sicl", "Standard Individual Trade Control Licence"),
                    ("sitl", "Standard Individual Transhipment Licence"),
                    ("f680", "MOD F680 Clearance"),
                    ("exhc", "MOD Exhibition Clearance"),
                    ("gift", "MOD Gifting Clearance"),
                    ("cre", "HMRC Query"),
                    ("gqy", "Goods Query"),
                    ("eua", "End User Advisory Query"),
                ],
                max_length=5,
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="casetype",
            name="sub_type",
            field=models.CharField(
                choices=[
                    ("standard", "Standard Licence"),
                    ("open", "Open Licence"),
                    ("hmrc", "HMRC Query"),
                    ("end_user_advisory", "End User Advisory Query"),
                    ("goods", "Goods Query"),
                    ("exhibition_clearance", "MOD Exhibition Clearance"),
                    ("gifting_clearance", "MOD Gifting Clearance"),
                    ("f680_clearance", "MOD F680 Clearance"),
                ],
                max_length=35,
            ),
        ),
        migrations.AddField(
            model_name="casetype",
            name="type",
            field=models.CharField(choices=[("application", "Application"), ("query", "Query")], max_length=35),
        ),
        migrations.AddField(
            model_name="casetype",
            name="id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="case",
            name="case_type",
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.DO_NOTHING, to="cases.CaseType"),
        ),
    ]