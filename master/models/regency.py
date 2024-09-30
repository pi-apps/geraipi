from django.db import models

from master.models.provinsi import Provinsi


class Regency(models.Model):
    code = models.CharField(max_length=255)
    province_code = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code
