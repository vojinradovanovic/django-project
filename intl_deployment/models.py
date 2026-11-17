from django.db import models
from django_countries.fields import CountryField

### MODELS ###

class Country(models.Model):
    country_name = CountryField()

class Region(models.Model):
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=100)

class TaxBracket(models.Model):
    region_name = models.ForeignKey(Region, on_delete=models.CASCADE)
    tax_rate = models.DecimalField(max_digits = 4, decimal_places = 2)  # tax percentage, from 00.00 to 99.99,
                                                                        # two decimal places

    min_salary_threshold = models.PositiveIntegerField()   # tax is applicable above this threshold