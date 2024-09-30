from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)
    wiki_id = models.CharField(max_length=100)
