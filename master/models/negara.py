from django.db import models


class Negara(models.Model):
    kode = models.CharField(max_length=50)
    nama = models.CharField(max_length=100)
