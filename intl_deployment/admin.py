from django.contrib import admin

from .models import *

# define admins
class CountryAdmin(admin.ModelAdmin):
    list_display = ["country", "currency"]

class RegionAdmin(admin.ModelAdmin):
    list_display = ["region_name", "country"]
    list_filter = ["country"]
    fields = ["region_name", "country"]

# Register models
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(TaxBracket)