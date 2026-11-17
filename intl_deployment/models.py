from django.db import models
from django_countries.fields import CountryField

### MODELS ###

class Country(models.Model):
    country_name = CountryField()