from django.db import models


class Provinsi(models.Model):
    code = models.CharField(max_length=255)
    nama = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code
