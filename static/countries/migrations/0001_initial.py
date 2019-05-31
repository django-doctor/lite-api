# Generated by Django 2.2 on 2019-05-08 14:45
import csv

from django.db import migrations, models


def init(apps, schema_editor):
    # We can't import the Queue model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Country = apps.get_model('countries', 'Country')
    if not Country.objects.all():
        with open('lite-content/lite-api/countries.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)  # skip the headers
            for row in reader:
                country = Country(id=row[0], name=row[1], report_name=row[2])
                country.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.IntegerField(primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('report_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RunPython(init),
    ]