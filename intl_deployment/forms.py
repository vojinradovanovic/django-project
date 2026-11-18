from django import forms
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

    class LivingStatus(forms.TextChoices):    # local enum class
        SOLE = "Single, no children"
        COMMON = "Married/Single, with children"

    living_status = forms.CharField(max_length=10, choices=LivingStatus.choices)

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

    salary = forms.DecimalField(label="Annual salary",
        min_value=0
    )

    bonus = forms.DecimalField(label="Annual bonus", min_value=0, required=False)

    # ------------ benefits ------------

    housing = forms.DecimalField()

    relocation_allowance = forms.DecimalField()

    moving_costs = forms.DecimalField()

    temporary_housing = forms.DecimalField()

    # ------------ other ------------

    exchange_rate = forms.DecimalField()