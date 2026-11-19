from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from .models import Country, Region, City

from dateutil.relativedelta import relativedelta

### FORMS ###
class QueryForm(forms.Form):
    # ------------ moving data ------------

    home_country = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    home_city = forms.ModelChoiceField(
        queryset=City.objects.all()
    )

    host_country = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    host_city = forms.ModelChoiceField(
        queryset=City.objects.all()
    )

    start_date = forms.DateField(
        input_formats=['%Y-%m-%d'],

        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )

    end_date = forms.DateField(
        input_formats=['%Y-%m-%d'],

        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )

    # ------------ employee data ------------

    citizenship = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    class LivingStatus(models.TextChoices):    # local enum class
        SOLE = "Sole", "Single, no children"
        COMMON = "Common", "Married/Single, with children"

    living_status = forms.ChoiceField(choices=LivingStatus.choices)

    years_of_work = forms.DecimalField(decimal_places=1)

    # ------------ employer data ------------

    home_employer_country = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    host_employer_country = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    host_employer_payroll_country = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    # ------------ salary ------------

    salary = forms.DecimalField(label="Annual salary", min_value=0)

    bonus = forms.DecimalField(label="Annual bonus", min_value=0, required=False)

    # ------------ benefits ------------

    housing = forms.DecimalField(label="Housing pcm (host country currency)")

    relocation_allowance = forms.DecimalField(label="Relocation allowance, 1st year (HOME country currency)")

    moving_costs = forms.DecimalField(label="Moving costs, 1st year (host country currency)")

    temporary_housing = forms.DecimalField(label="Temporary housing, 1st year (host country currency)")

    # ------------ other ------------

    exchange_rate = forms.DecimalField()



    # ------------ cleaning functions ------------

    def clean_home_country(self):
        home_country = self.cleaned_data["home_country"]

        if home_country.country.name != "Switzerland":
            raise ValidationError("Only Switzerland is supported here!", code="unsupported")

        return home_country

    def clean_citizenship(self):
        citizenship = self.cleaned_data["citizenship"]

        if citizenship.country.name != "Switzerland":
            raise ValidationError("Only Switzerland is supported here!", code="unsupported")

        return citizenship

    def clean_living_status(self):
        living_status = self.cleaned_data["living_status"]

        if living_status != self.LivingStatus.SOLE:
            raise ValidationError("Only \"%(single)s\" is supported here!", code="unsupported",
                                    params = {"single": self.LivingStatus.SOLE.label})

        return living_status

    def clean_exchange_rate(self):
        exchange_rate = self.cleaned_data["exchange_rate"]

        if exchange_rate <= 0:
            raise ValidationError("Exchange rate must be positive!", code="invalid")

        return exchange_rate

    def clean(self):
        cleaned_data = super().clean()

        # get needed fields
        home_country = cleaned_data["home_country"]
        host_country = cleaned_data["host_country"]

        home_city = cleaned_data["home_city"]
        host_city = cleaned_data["host_city"]

        start_date = cleaned_data["start_date"]
        end_date = cleaned_data["end_date"]

        # match cities to countries
        if home_city.region.country != home_country:
            self.add_error("home_city",
                            ValidationError("Home city must be within home country!", code="invalid"))

        if host_city.region.country != host_country:
            self.add_error("host_city",
                            ValidationError("Host city must be within host country!", code="invalid"))

        # compare dates
        if start_date >= end_date:
            self.add_error("start_date",
                            ValidationError("Start date must be before the end date!", code="invalid"))

        # only relative difference between dates of <= 2 years is supported
        date_difference = relativedelta(end_date, start_date)
        if not(date_difference.years < 2):
            self.add_error("end_date",
                            ValidationError("Only periods no longer than 2 years are supported!", code="unsupported"))

        # compare countries
        if home_country == host_country:
            self.add_error("host_country",
                            ValidationError("Home country and host country must be different!", code="invalid"))

        return cleaned_data