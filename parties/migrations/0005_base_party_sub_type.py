# Generated by Django 2.2.8 on 2020-01-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parties", "0004_third_party_role"),
    ]

    operations = [
        migrations.RemoveField(model_name="consignee", name="sub_type",),
        migrations.RemoveField(model_name="enduser", name="sub_type",),
        migrations.RemoveField(model_name="thirdparty", name="sub_type",),
        migrations.RemoveField(model_name="ultimateenduser", name="sub_type",),
        migrations.AddField(
            model_name="party",
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