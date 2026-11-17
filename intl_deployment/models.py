from django.db import models
from django_countries.fields import CountryField

### MODELS ###

class TaxAuthority(models.Model):
    name = models.CharField(max_length=100)

    class Level(models.TextChoices):    # local enum class
        FEDERAL = "Federal"
        REGIONAL = "Regional"
        LOCAL = "Local"

    level = models.CharField(max_length=10, choices=Level.choices)

    def __str__(self):
        return self.name

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

class TaxBracket(models.Model):
    tax_authority = models.ForeignKey(TaxAuthority, on_delete=models.CASCADE)
    tax_rate = models.DecimalField(max_digits = 4, decimal_places = 2)  # tax percentage, from 00.00 to 99.99,
                                                                        # two decimal places

    min_salary_threshold = models.PositiveIntegerField()   # tax is applicable above this threshold

    source = models.URLField(max_length=255, null=True)

    def __str__(self):
        return str(self.tax_authority.name) + ", " + str(self.tax_rate) + "%"