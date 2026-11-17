from django.db import models
from django_countries.fields import CountryField

### MODELS ###

class Country(models.Model):
    country_name = CountryField()

class Region(models.Model):
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE)