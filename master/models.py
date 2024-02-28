from django.db import models
from solo.models import SingletonModel


# Create your models here.
class Provinsi(models.Model):
    code = models.CharField(max_length=255)
    nama = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code


class Regency(models.Model):
    code = models.CharField(max_length=255)
    province_code = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code


class Distric(models.Model):
    code = models.CharField(max_length=255)
    regency_code = models.ForeignKey(Regency, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code


class Village(models.Model):
    code = models.CharField(max_length=255)
    district_code = models.ForeignKey(Distric, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.code


class SettingWebsite(models.Model):
    SETTING_NAMA = [
        (1, "api_key"),
        (2, "wallet_private"),
        (3, "pajak_beli"),
        (4, "pajak_withdrawl"),
    ]
    nama_pengaturan = models.IntegerField(choices=SETTING_NAMA)
    setting_value = models.CharField(max_length=255)

    def __str__(self):
        return self.setting_value


class ConfigurationWebsite(SingletonModel):
    api_key_pi = models.CharField(blank=True, null=True, max_length=255)
    wallet_private_pi = models.CharField(blank=True, null=True, max_length=255)
    pajak_beli = models.FloatField(default=0)
    pajak_withdrawl = models.FloatField(default=0)
    koin_website = models.FloatField(default=0)


class HistoriTampung(models.Model):
    tanggal = models.DateTimeField(auto_now=True)
    jumlah = models.FloatField(default=0)
    success = models.BooleanField(default=False)


# class Tampung(models.Model):
#     history_tampung = models.CharField(max_length=)
