from django.db import models
from master.utils import SOURCE_REQUEST


class Expedisi(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255)
    url_request = models.URLField(null=True, blank=True)
    source_request = models.IntegerField(choices=SOURCE_REQUEST, default=1)

    def __str__(self):
        return self.nama
