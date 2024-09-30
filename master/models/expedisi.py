from django.db import models


class Expedisi(models.Model):
    SOURCE_REQUEST = [
        (1, "Raja Ongkir"),
        (2, "Biteship"),
    ]
    code = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255)
    url_request = models.URLField(null=True, blank=True)
    source_request = models.IntegerField(choices=SOURCE_REQUEST, default=1)

    def __str__(self):
        return self.nama

