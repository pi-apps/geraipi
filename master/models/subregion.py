from django.db import models

from master.models.region import Region


class SubRegion(models.Model):
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    wiki_id = models.CharField(max_length=100)
