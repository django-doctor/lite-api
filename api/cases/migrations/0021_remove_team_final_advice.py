# Generated by Django 2.2.11 on 2020-05-07 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0020_migrate_team_final_advice"),
    ]

    operations = [
        migrations.DeleteModel(name="FinalAdvice",),
        migrations.DeleteModel(name="TeamAdvice",),
    ]