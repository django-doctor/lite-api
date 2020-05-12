# Generated by Django 2.2.11 on 2020-05-04 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0016_auto_20200502_2245"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ecjuquery",
            name="query_type",
            field=models.CharField(
                choices=[
                    ("ecju_query", "Standard query"),
                    ("pre_visit_questionnaire", "Pre-visit question"),
                    ("compliance_actions", "Compliance action"),
                ],
                default="ecju_query",
                max_length=50,
            ),
        ),
    ]
