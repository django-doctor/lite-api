from django.db import transaction

from static.countries.models import Country
from static.management.SeedCommand import SeedCommand, SeedCommandTest


COUNTRIES_FILE = "lite_content/lite-api/countries.csv"


class Command(SeedCommand):
    """
    pipenv run ./manage.py seedcountries
    """

    help = "Seeds all countries"
    info = "Seeding countries"
    success = "Successfully seeded countries"
    seed_command = "seedcountries"

    @transaction.atomic
    def operation(self, *args, **options):
        csv = self.read_csv(COUNTRIES_FILE)
        self.update_or_create(Country, csv)
        self.delete_unused_objects(Country, csv)


class SeedCountriesTests(SeedCommandTest):
    def test_seed_countries(self):
        self.seed_command(Command)
        self.assertTrue(Country.objects.count() == len(Command.read_csv(COUNTRIES_FILE)))