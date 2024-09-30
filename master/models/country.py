from django.db import models

from master.models.region import Region
from master.models.subregion import SubRegion


class Country(models.Model):
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    subregion_id = models.ForeignKey(SubRegion, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    iso3 = models.CharField(max_length=50, blank=True, null=True)
    iso2 = models.CharField(max_length=50, blank=True, null=True)
    numeric_code = models.CharField(max_length=50, blank=True, null=True)
    phone_code = models.CharField(max_length=50, blank=True, null=True)
    capital = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    currency_name = models.CharField(max_length=50, blank=True, null=True)
    currency_symbol = models.CharField(max_length=50, blank=True, null=True)
    tld = models.CharField(max_length=50, blank=True, null=True)
    native = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    timezones = models.TextField(blank=True, null=True, default=[])
    is_active = models.BooleanField(default=True)
