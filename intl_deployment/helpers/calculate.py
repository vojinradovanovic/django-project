from ..models import *

def calculate_swiss_tax(base, region, city):
    # initialisations: tax authorities, tax brackets, taxes
    tax_authorities = {
        "federal": Country.objects.filter(country=CountryField("Switzerland")).tax_authority,
        "cantonal": Region.objects.filter(region=region).tax_authority,
        "municipal": City.objects.filter(city=city).tax_authority
    }
    tax_brackets = {
        key: TaxBracket.objects.filter(tax_authority=tax_authorities[key])
                .order_by("-min_salary_threshold")
                
                for key in tax_authorities.keys
    }
    taxes = {
        key: 0. for key in tax_authorities.keys
    }

    # calculate federal tax
    taxes["federal"] = traverse_tax_brackets(base, tax_brackets["federal"])

    # calculate cantonal tax
    taxes["cantonal"] = traverse_tax_brackets(base, tax_brackets["cantonal"])

    # calculate municipal tax in the case of Zurich
    if city.name == "City of Zurich":
        # calculate based on multipliers: 0.95 for cantonal and 1.19 for municipal
        base_cantonal_tax = taxes["cantonal"]

        taxes["cantonal"] = base_cantonal_tax * 0.95
        taxes["municipal"] = base_cantonal_tax * 1.19

    return sum(taxes.values())

def traverse_tax_brackets(base, tax_brackets):
    total_tax = 0

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
    # initialisations: tax authorities, tax brackets
    tax_authority = Region.objects.filter(region=region).tax_authority

    tax_brackets = TaxBracket.objects.filter(tax_authority=tax_authority)