# Generated by Django 2.2.8 on 2020-01-27 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0002_auto_20200115_1116"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casestatuscasetype",
            name="type",
            field=models.CharField(
                choices=[
                    ("application", "Application"),
                    ("goods_query", "Product Query"),
                    ("end_user_advisory_query", "End User Advisory Query"),
                    ("hmrc_query", "HMRC Query"),
                    ("exhibition_clearance", "MOD Exhibition Clearance"),
                ],
                max_length=35,
            ),
        ),
    ]