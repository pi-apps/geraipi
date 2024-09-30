from django.db import models

from master.models.regency import Regency


class Distric(models.Model):
    code = models.CharField(max_length=255)
    regency_code = models.ForeignKey(Regency, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code
