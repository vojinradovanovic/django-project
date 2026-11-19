from ..forms import QueryForm
from .calculate import calculate_tax, calculate_social_security

def extract_from_QueryForm(query_form):
    input = {
        # ------------ moving data ------------

        "home_country": query_form.cleaned_data["home_country"],
        "home_city": query_form.cleaned_data["home_city"],
        "home_region": query_form.cleaned_data["home_city"].region,

        "host_country": query_form.cleaned_data["host_country"],
        "host_city": query_form.cleaned_data["host_city"],
        "host_region": query_form.cleaned_data["host_city"].region,

        "start_date": query_form.cleaned_data["start_date"],
        "end_date": query_form.cleaned_data["end_date"],

        # ------------ employee data ------------

        "citizenship": query_form.cleaned_data["citizenship"],
        "living_status": query_form.cleaned_data["living_status"],
        "years_of_work": query_form.cleaned_data["years_of_work"],

        # ------------ employer data ------------

        "home_employer_country": query_form.cleaned_data["home_employer_country"],
        "host_employer_country": query_form.cleaned_data["host_employer_country"],
        "host_employer_payroll_country": query_form.cleaned_data["host_employer_payroll_country"],

        # ------------ salary ------------

        "salary": query_form.cleaned_data["salary"],
        "bonus": query_form.cleaned_data["bonus"],

        # ------------ benefits ------------

        "housing": query_form.cleaned_data["housing"],
        "relocation_allowance": query_form.cleaned_data["relocation_allowance"],
        "moving_costs": query_form.cleaned_data["moving_costs"],
        "temporary_housing": query_form.cleaned_data["temporary_housing"],

        # ------------ other ------------

        "exchange_rate": query_form.cleaned_data["exchange_rate"]
    }

    return input

def generate_cost_estimate_data(input):
    # wrap data for output
    home_pay = {
        "salary": input["salary"],
        "bonus": input["bonus"]
    }

    assignment_benefits = {
        "housing": input["housing"],
        "relocation_allowance": input["relocation_allowance"],
        "moving_costs": input["moving_costs"],
        "temporary_housing": input["temporary_housing"]
    }

    # calculate base pay
    home_base_pay = sum(home_pay.values())       #TODO: taxable in Switzerland, UK, etc

    deductions = {
        "home_income_tax": calculate_tax(home_base_pay, input["home_country"], input["home_region"], input["home_city"]),
        "home_social_security": calculate_social_security(home_base_pay, input["home_country"])
    }

    # calculate taxable pay in host country
    host_base_pay = (home_base_pay - sum(deductions.values())) / input["exchange_rate"]

    host_tax = {
        "host_income_tax": calculate_tax(host_base_pay, input["host_country"], input["host_region"], input["host_city"])
    }

    # other useful information
    other = {
        "home_country": input["home_country"],
        "host_country": input["host_country"]
    }

    # redefine data for output
    data = {
        "home_pay": home_pay,
        "assignment_benefits": assignment_benefits,
        "host_tax": host_tax,
        "deductions": deductions,
        "other": other
    }
    
    return data