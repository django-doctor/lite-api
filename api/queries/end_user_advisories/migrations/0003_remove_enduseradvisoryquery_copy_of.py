# Generated by Django 2.2.8 on 2020-02-11 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("end_user_advisories", "0002_enduseradvisoryquery_end_user"),
    ]

    operations = [
        migrations.RemoveField(model_name="enduseradvisoryquery", name="copy_of",),
    ]