# Generated by Django 2.2.13 on 2020-07-03 09:26

from django.db import migrations

from api.licences.enums import LicenceStatus


def convert_licence_status(apps, schema_editor):
    Licence = apps.get_model("licences", "Licence")

    for licence in Licence.objects.all():
        if licence.is_complete:
            licence.status = LicenceStatus.ISSUED
        else:
            licence.status = LicenceStatus.DRAFT
        licence.save()


def reverse_licence__status(apps, schema_editor):
    Licence = apps.get_model("licences", "Licence")

    for licence in Licence.objects.all():
        if licence.status == LicenceStatus.ISSUED:
            licence.is_complete = True
        else:
            licence.is_complete = False
        licence.save()


class Migration(migrations.Migration):

    dependencies = [
        ("licences", "0007_licence_status"),
    ]

    operations = [
        migrations.RunPython(convert_licence_status, reverse_code=reverse_licence__status),
    ]
