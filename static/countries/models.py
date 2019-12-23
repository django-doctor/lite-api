from django.db import models

from flags.models import Flag


class Country(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)  # Country Code
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    flags = models.ManyToManyField(Flag, related_name="countries")
