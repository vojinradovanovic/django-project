from decimal import Decimal
from django.db import models

from dateutil.relativedelta import relativedelta

def rate_to_multiplyer(tax_rate: models.DecimalField):
    """Converts tax rates, given as %, to a multiplyer"""

    return tax_rate / Decimal("100")

def determine_ss_residency(home_country, host_country, start_date, end_date):
    if host_country.country.name == "United Kingdom":
        if home_country.country.name == "Switzerland":
            # calculate the number of years
            date_difference = relativedelta(end_date, start_date)

            years = date_difference.years
            months = date_difference.months
            days = date_difference.days

            # 2 years, 0 months, 0 days is produced between the same dates of 2 different years
            if years<2:
                return home_country

            else:
                return host_country