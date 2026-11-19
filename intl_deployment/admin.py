from django.contrib import admin

from .models import *

# define admins
class CountryAdmin(admin.ModelAdmin):
    list_display = ["country", "currency", "tax_authority"]

class RegionAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "tax_authority"]
    list_filter = ["country"]
    fields = ["name", "country", "tax_authority"]

class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "tax_authority"]
    list_filter = ["region"]
    fields = ["name", "region", "tax_authority"]

# Register models
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(TaxAuthority)
admin.site.register(TaxBracket)
admin.site.register(SocialSecurityTax)