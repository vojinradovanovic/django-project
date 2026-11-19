from django.db import models

from .location import Country

### MODELS ###

class SocialSecurityTax(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    tax_rate = models.DecimalField(max_digits = 4, decimal_places = 2)  # tax percentage, from 00.00 to 99.99,
                                                                        # two decimal places

    max_taxable_income = models.PositiveIntegerField()  # this is the maximum income which is taxable, e.g. Swiss unemployment

    description = models.CharField(max_length=100)

    source = models.URLField(max_length=255, null=True)

    def __str__(self):
        return str(self.country.country.name) + ", " + str(self.description)