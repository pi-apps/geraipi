from django.db import models


class HistoriTampung(models.Model):
    tanggal = models.DateTimeField(auto_now=True)
    jumlah = models.FloatField(default=0)
    success = models.BooleanField(default=False)
