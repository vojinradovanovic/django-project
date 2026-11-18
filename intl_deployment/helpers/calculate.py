from decimal import Decimal
from ..models import *



def calculate_tax(base, country, region, city):
    if country.country.name == "Switzerland":
        return calculate_swiss_tax(base, region, city)

    elif country.country.name == "United Kingdom":
        return calculate_uk_tax(base, region)



def calculate_swiss_tax(base, region, city):
    # initialisations: tax authorities, tax brackets, taxes
    tax_authorities = {
        "federal": Country.objects.get(country="CH").tax_authority,
        "cantonal": region.tax_authority,
        "municipal": city.tax_authority
    }
    tax_brackets = {
        key: TaxBracket.objects.filter(tax_authority=tax_authorities[key])
                .order_by("-min_salary_threshold")
                
                for key in tax_authorities.keys()
    }
    taxes = {
        key: 0. for key in tax_authorities.keys()
    }

    print("Hello")
    print(tax_authorities)

    # calculate federal tax
    taxes["federal"] = traverse_tax_brackets(base, tax_brackets["federal"])

    # calculate cantonal tax
    taxes["cantonal"] = traverse_tax_brackets(base, tax_brackets["cantonal"])

    # calculate municipal tax in the case of Zurich
    if city.name == "City of Zurich":
        # calculate based on multipliers: 0.95 for cantonal and 1.19 for municipal
        base_cantonal_tax = taxes["cantonal"]

        taxes["cantonal"] = base_cantonal_tax * Decimal("0.95")
        taxes["municipal"] = base_cantonal_tax * Decimal("1.19")

    return sum(taxes.values())

def traverse_tax_brackets(base, tax_brackets):
    total_tax = Decimal("0")

    for tax_bracket in tax_brackets:
        # extract data
        threshold = tax_bracket.min_salary_threshold
        tax_rate = tax_bracket.tax_rate

        if base > threshold:
            # add tax
            total_tax += (base - threshold) * tax_rate

            # lower base for next tax bracket
            base = threshold

    return total_tax



def calculate_uk_tax(base, region):
    # initialisations: tax authorities, tax brackets, taxes
    tax_authority = Region.objects.filter(region=region).tax_authority

    tax_brackets = TaxBracket.objects.filter(tax_authority=tax_authority) \
                    .order_by("-min_salary_threshold")

    previous_tax = 0
    final_tax = 0

    # initialisations: other
    max_untaxable_income = 12570
    lowering_threshold = pow(10, 5)

    # tax loop
    while True:
        # synchronise
        previous_tax = final_tax

        # calculate tax
        # initial
        final_tax = traverse_tax_brackets(base, tax_brackets)

        # lower untaxed portion if needed
        final_tax += min(max_untaxable_income, (base-lowering_threshold)/2)

        if abs(final_tax-previous_tax)<1:
            break

    return final_tax