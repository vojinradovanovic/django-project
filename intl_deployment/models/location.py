from django.db import models
from django_countries.fields import CountryField

from .taxes import TaxAuthority

### MODELS ###

class Country(models.Model):
    country = CountryField()
    currency = models.CharField(max_length=3)
    tax_authority = models.ForeignKey(TaxAuthority, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.country.name

class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tax_authority = models.ForeignKey(TaxAuthority, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tax_authority = models.ForeignKey(TaxAuthority, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name