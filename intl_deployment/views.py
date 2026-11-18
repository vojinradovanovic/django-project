from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import QueryForm

### VIEWS ###

def cost_estimate(request):

    # if form has been filled out
    if request.method == "POST":
        form = QueryForm(request.POST)  # populate form
        
        if form.is_valid():
            # unpack data from form.cleaned_data

            # ------------ moving data ------------

            home_country = form.cleaned_data["home_country"]
            home_region = form.cleaned_data["home_region"]
            home_city = form.cleaned_data["home_city"]

            host_country = form.cleaned_data["host_country"]
            host_region = form.cleaned_data["host_region"]
            host_city = form.cleaned_data["host_city"]

            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            # ------------ employee data ------------

            citizenship = form.cleaned_data["citizenship"]
            living_status = form.cleaned_data["living_status"]
            years_of_work = form.cleaned_data["years_of_work"]

            # ------------ employer data ------------

            home_employer_country = form.cleaned_data["home_employer_country"]
            host_employer_country = form.cleaned_data["host_employer_country"]
            host_employer_payroll_country = form.cleaned_data["host_employer_payroll_country"]

            # ------------ salary ------------

            salary = form.cleaned_data["salary"]
            bonus = form.cleaned_data["bonus"]

            # ------------ benefits ------------

            housing = form.cleaned_data["housing"]
            relocation_allowance = form.cleaned_data["relocation_allowance"]
            moving_costs = form.cleaned_data["moving_costs"]
            temporary_housing = form.cleaned_data["temporary_housing"]

            # ------------ other ------------

            exchange_rate = form.cleaned_data["exchange_rate"]

            # wrap data for output
            home_pay = {
                "salary": salary,
                "bonus": bonus
            }

            assignment_benefits = {
                "housing": housing,
                "relocation_allowance": relocation_allowance,
                "moving_costs": moving_costs,
                "temporary_housing": temporary_housing
            }

            host_tax = {}

            deductions = {}

            # redefine data for output
            data = {
                "home_pay": home_pay,
                "assignment_benefits": assignment_benefits,
                "host_tax": host_tax,
                "deductions": deductions
            }

    # for any other request, create a blank form
    else:
        form = QueryForm()

    return render(request, "intl_deployment/cost_estimate.html", {"form": form, "data": data})

def immigration(request):
    return HttpResponse("Immigration goes here.")