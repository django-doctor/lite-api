# Generated by Django 2.2.13 on 2020-07-03 09:40

from django.db import migrations

from licences.enums import LicenceStatus


def convert_good_on_application_to_good_on_licence(apps, schema_editor):
    GoodOnApplication = apps.get_model("applications", "GoodOnApplication")
    GoodOnLicence = apps.get_model("licences", "GoodOnLicence")
    Licence = apps.get_model("licences", "Licence")

    for good_on_application in GoodOnApplication.objects.filter(licenced_quantity__isnull=False):
        licence = Licence.objects.filter(application=good_on_application.application).first()
        if licence:
            GoodOnLicence.objects.create(
                good=good_on_application,
                licence=licence,
                usage=good_on_application.usage,
                quantity=good_on_application.licenced_quantity,
                value=good_on_application.licenced_value,
            )


def reverse_good_on_application_to_good_on_licence(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [("licences", "0010_goodonlicence"), ("applications", "0025_auto_20200414_1617")]

    operations = [
        migrations.RunPython(
            convert_good_on_application_to_good_on_licence, reverse_code=reverse_good_on_application_to_good_on_licence
        ),
    ]
