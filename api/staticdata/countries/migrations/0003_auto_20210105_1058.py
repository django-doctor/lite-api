# Generated by Django 2.2.17 on 2021-01-05 10:58

from django.db import migrations


country_map_lite_to_spire = {
    "Burma": "Myanmar",
    "Cocos (Keeling) Islands": "Cocos Islands",
    "Congo (Democratic Republic)": "Congo, Democratic Republic of",
    "Curaçao": "Curacao",
    "Czechia": "Czech Republic",  # this is as per SPIRE, but SPIRE is out of date
    "Heard Island and McDonald Islands": "Heard and McDonald Islands",
    "Midway Islands": "Midway Island",
    "New Caledonia": "New Caledonia and Dependencies",
    "Norfolk Island": "Norfolk Island",
    "North Korea": "Korea, North",
    "Pitcairn, Henderson, Ducie and Oeno Islands": "Pitcairn Island",
    "Ras al-Khaimah": "Ras al Khaimah",
    "Réunion": "Reunion",
    "Saba": "Saba",
    "Saint Barthélemy": "St Barthelemy",
    "Saint Helena": "St Helena",
    "Saint Pierre and Miquelon": "St Pierre and Miquelon",
    "Saint-Martin (French part)": "St Martin, North",
    "Sint Eustatius": "St Eustatius",
    "Sint Maarten (Dutch part)": "St Maarten, South",
    "South Korea": "Korea, South",
    "South Sudan": "Sudan, South",
    "St Kitts and Nevis": "St Kitts And Nevis",
    "St Vincent": "St Vincent and the Grenadines",
    "Suriname": "Surinam",
    "Svalbard and Jan Mayen": "Svalbard Archipelago",
    "The Bahamas": "Bahamas",
    "The Gambia": "Gambia",
    "UK Continental Shelf": "Continental Shelf United Kingdom Sector",
    "Umm al-Quwain": "United Arab Emirates",
    "Wallis and Futuna": "Wallis and Futuna",
    "Åland Islands": "Aland Islands",
}

# noteworthy: LITE has some countries that SPIRE does not:
# "Akrotiri"  # part of Cyprus?
# "Dhekelia"  # part of Cyprus?
# "East Timor"  # not in SPIRE. historically part of Indonesia?
# "Navassa Island"  # a small uninhabited island in the Caribbean Sea ?
# "Western Sahara"  # disputed territory


def forwards(apps, schema_editor):
    Country = apps.get_model("countries", "Country")
    for country in Country.objects.exclude(name__isnull=True):
        if country.name in country_map_lite_to_spire:
            country.report_name = country_map_lite_to_spire[country.name]
        else:
            country.report_name = country.name
        country.save()


class Migration(migrations.Migration):

    dependencies = [
        ("countries", "0002_country_report_name"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
