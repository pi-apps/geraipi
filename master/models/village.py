from django.db import models

from master.models.distric import Distric


class Village(models.Model):
    code = models.CharField(max_length=255)
    district_code = models.ForeignKey(Distric, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code
