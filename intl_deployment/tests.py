from django.test import TestCase
from .forms import QueryForm
from .models.location import *

# Create your tests here.
class QueryFormTests(TestCase):

    def test_validity_of_test_case(self):
        # populate databases to perform the test
        self.populate_databases()

        form = QueryForm({
            "home_country": self.switzerland,
            "home_city": self.city_of_zurich,

            "host_country": self.uk,
            "host_city": self.london,

            "start_date": "2026-04-06",
            "end_date": "2028-04-05",

            "citizenship": self.switzerland,
            "living_status": "Sole",
            "years_of_work": 3,

            "home_employer_country": self.switzerland,
            "host_employer_country": self.uk,
            "host_employer_payroll_country": self.switzerland,

            "salary": 150000,
            "bonus": 20000,

            "housing": 3000,
            "relocation_allowance": 5000,
            "moving_costs": 6000,
            "temporary_housing": 4000,

            "exchange_rate": 1.1
        })

        self.assertTrue(form.is_valid(), form.errors)

    def populate_databases(self):
        # population is done without tax authorities for simplicity

        # create countries
        self.switzerland = Country.objects.create(country="CH", currency="CHF")
        self.uk = Country.objects.create(country="GB", currency="GBP")

        # create regions
        self.zurich_canton = Region.objects.create(name="Zurich", country=self.switzerland)
        self.england = Region.objects.create(name="England", country=self.uk)

        # create cities
        self.city_of_zurich = City.objects.create(name="City of Zurich", region=self.zurich_canton)
        self.london = City.objects.create(name="London", region=self.england)