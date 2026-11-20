from ..forms import QueryForm
from .calculate import calculate_tax, calculate_social_security
from .helpers import determine_ss_residency

from datetime import timedelta
from dateutil.relativedelta import relativedelta

from decimal import Decimal, ROUND_HALF_UP

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

    # create dictionary for aggregating sources
    sources = {
        "ss_residency": set(),
        "home_income_tax": set(),
        "home_social_security": set(),
        "home_income_tax": set(),
        "home_income_tax_first_year": set(),
        "other": set()
    }
    # calculate base pay
    home_base_pay = sum(home_pay.values())

    # establish social security residency and tax
    ss_residency_country, sources["ss_residency"] = determine_ss_residency(input["home_country"], input["host_country"],
                                                        input["start_date"], input["end_date"])

    home_income_tax, sources["home_income_tax"] = calculate_tax(home_base_pay, input["home_country"],
                                                                input["home_region"], input["home_city"])

    home_social_security, sources["home_social_security"] = calculate_social_security(home_base_pay,
                                                                                    input["home_country"], ss_residency_country)

    deductions = {
        "home_income_tax": home_income_tax,
        "home_social_security": home_social_security
    }

    # calculate taxable pay in host country
    host_base_pay = (home_base_pay - sum(deductions.values())) / input["exchange_rate"]

    # calculate taxable relocation allowance and add source
    taxable_relocation = max(Decimal("0"), assignment_benefits["moving_costs"] \
                                            + assignment_benefits["temporary_housing"] \
                                            - Decimal("8000"))
    sources["other"].add("https://www.gov.uk/expenses-and-benefits-relocation/whats-exempt")

    # add benefits
    host_base_pay += Decimal("12") * assignment_benefits["housing"] # housing is pcm
    host_first_year_extra = assignment_benefits["relocation_allowance"] / input["exchange_rate"] \
                            + taxable_relocation

    host_income_tax, sources["host_income_tax"] = \
            calculate_tax(host_base_pay,
                            input["host_country"], input["host_region"], input["host_city"])

    host_income_tax_first_year, sources["host_income_tax_first_year"] = \
            calculate_tax(host_base_pay + host_first_year_extra,
                        input["host_country"], input["host_region"], input["host_city"])

    host_social_security, sources["host_social_security"] = calculate_social_security(home_base_pay,
                                                                                      input["host_country"], ss_residency_country)

    host_tax = {
        "host_income_tax": host_income_tax,
        "host_social_security": host_social_security,
        "first_year_income_tax": host_income_tax_first_year - host_income_tax
    }

    # calculate taxes for the final figure
    total_taxable_period = relativedelta(input["end_date"], input["start_date"])
    total_tax = 0

    if total_taxable_period.years < 1:      # 1 year 0 months 0 days is included in this, adjustments are made with timedelta
        total_taxable_period = relativedelta(input["end_date"] + timedelta(days=1), input["start_date"])
        scaling = total_taxable_period.years \
                    + total_taxable_period.months / 12 \
                    + total_taxable_period.days / 360
        total_tax +=  Decimal(f"{scaling}") * host_income_tax_first_year

    else:
        total_tax += host_income_tax_first_year

        total_taxable_period = relativedelta(input["end_date"] + timedelta(days=1), input["start_date"])
        scaling = total_taxable_period.years - 1 \
                    + total_taxable_period.months / 12 \
                    + total_taxable_period.days / 360

        total_tax += Decimal(f"{scaling}") * host_income_tax

    # round tax
    total_tax = total_tax.quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    # set aggregate tax data
    aggregate_tax_data = {
        "total_host_tax": total_tax,
        "as_percentage_of_host_base": (total_tax / host_base_pay * Decimal("100")).
                                        quantize(Decimal("0"), rounding=ROUND_HALF_UP)
    }



    # set assumptions
    assumptions = ["Stable exchange rate for the entire assignment period",
                   "2026 tax rates for the entire assignment period",
                   "Total income taxes scaled based on the duration of the assignment",
                   "Rounding is performed half up"]

    # other useful information
    other = {
        "home_country": input["home_country"],
        "host_country": input["host_country"],
        "sources": set().union(*sources.values()),
        "assumptions": assumptions
    }

    # redefine data for output
    data = {
        "home_pay": home_pay,
        "assignment_benefits": assignment_benefits,
        "host_tax": host_tax,
        "deductions": deductions,
        "aggregate_tax_data": aggregate_tax_data,
        "other": other
    }
    
    return data

def generate_immigration_data(input):
    data = {
        "visa": [],
        "business_visit": [],
        "passport_requirements": [],
        "employer_requirements": []
    }

    # the assumption is that this is similar to the test case, a Swiss citizen coming to the UK
    # for <= 2 years, so the output is generated to accommodate that

    # Passport requirements
    data["passport_requirements"].append({
        "description": "Valid passport;",
        "comments": ('The employee must hold a valid passport.\n' + \
                     'If it expires during the assignment, it should be renewed.'),
        "source": "https://www.gov.uk/guidance/visiting-the-uk-as-an-eu-eea-or-swiss-citizen"
    })

    # Work visa
    if input["host_country"].country.name == "United Kingdom":
        if input["home_country"].country.name == "Switzerland":
            data["visa"].append({
                "description": "Senior or Specialist Worker;",
                "comments": (""),
                "source": "https://www.gov.uk/senior-specialist-worker-visa"
            })

            data["employer_requirements"].append({
                "description": "Certificate of Sponsorship;",
                "comments": ('The UK sponsor must assign a valid Certificate\n' + \
                                'of Sponsorship to the employee.'),
                "source": "https://www.gov.uk/uk-visa-sponsorship-employers"
            })

    # Business visits
    if input["host_country"].country.name == "United Kingdom":
        if input["citizenship"].country.name == "Switzerland":
            data["business_visit"].append({
                "description": "Electronic Travel Authorisation;",
                "comments": ('Swiss citizens generally need an ETA for permitted\n' + \
                                'short business visits to the UK.'),
                "source": "https://www.gov.uk/eta"
            })

    # social security contributions for <= 2 years swiss arivals in the UK
    data["employer_requirements"].append({
        "description": 'Certificate of coverage\n(Swiss social security authority);',
        "comments": 'Not obliged to pay UK social security contributions if\n' + \
                    'the assignment period is 2 years at most;\n' + \
                    'the relevant authority is determined by place of residence',
        "source": "https://www.gov.uk/guidance/social-security-contributions-for-workers-coming-to-the-uk-from-the-eea-or-switzerland"
    })

    return data