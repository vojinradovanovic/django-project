from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from .models import Country, Region

### FORMS ###
class QueryForm(forms.Form):
    # ------------ moving data ------------

    home_country = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    home_region = forms.ModelChoiceField(
        queryset=Region.objects.all()
    )

    home_city = forms.CharField(max_length=200)

    host_country = forms.ModelChoiceField(
        queryset=Country.objects.all()
    )

    host_region = forms.ModelChoiceField(
        queryset=Region.objects.all()
    )

    host_city = forms.CharField(max_length=200)

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

    housing = forms.DecimalField()

    relocation_allowance = forms.DecimalField()

    moving_costs = forms.DecimalField()

    temporary_housing = forms.DecimalField()

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

    def clean(self):
        cleaned_data = super().clean()

        # get needed fields
        home_country = cleaned_data["home_country"]
        host_country = cleaned_data["host_country"]

        start_date = cleaned_data["start_date"]
        end_date = cleaned_data["end_date"]

        # compare dates
        if start_date >= end_date:
            self.add_error("start_date",
                            ValidationError("Start date must be before the end date!", code="invalid"))

        # compare countries
        if home_country == host_country:
            self.add_error("host_country",
                            ValidationError("Home country and host country must be different!", code="invalid"))

        return cleaned_data