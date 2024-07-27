from django.db import models
from solo.models import SingletonModel


class Region(models.Model):
    name = models.CharField(max_length=100)
    wiki_id = models.CharField(max_length=100)


class SubRegion(models.Model):
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    wiki_id = models.CharField(max_length=100)


class Country(models.Model):
    region_id = models.ForeignKey(
        Region, on_delete=models.CASCADE, blank=True, null=True
    )
    subregion_id = models.ForeignKey(
        SubRegion, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=100)
    iso3 = models.CharField(max_length=50, blank=True, null=True)
    iso2 = models.CharField(max_length=50, blank=True, null=True)
    numeric_code = models.CharField(max_length=50, blank=True, null=True)
    phone_code = models.CharField(max_length=50, blank=True, null=True)
    capital = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    currency_name = models.CharField(max_length=50, blank=True, null=True)
    currency_symbol = models.CharField(max_length=50, blank=True, null=True)
    tld = models.CharField(max_length=50, blank=True, null=True)
    native = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    timezones = models.TextField(blank=True, null=True, default=[])
    is_active = models.BooleanField(default=True)


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
    konfigurasi_firebase = models.FileField(
        blank=True, null=True, upload_to="konfigurasi/"
    )
    url_check_resi = models.URLField(blank=True, null=True)
    api_check_resi = models.CharField(blank=True, null=True, max_length=200)
    video_splash = models.FileField(
        blank=True, null=True, upload_to="splash", unique=True
    )

    api_biteship = models.CharField(blank=True, null=True, max_length=255)
    verification = models.CharField(blank=True, null=True, max_length=255)
    bypass_expedisi = models.BooleanField(default=False)


class HistoriTampung(models.Model):
    tanggal = models.DateTimeField(auto_now=True)
    jumlah = models.FloatField(default=0)
    success = models.BooleanField(default=False)


class Negara(models.Model):
    kode = models.CharField(max_length=50)
    nama = models.CharField(max_length=100)


class VoucherConfig(models.Model):
    generate_code = models.CharField(max_length=50)
    has_access_store = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


# class Tampung(models.Model):
#     history_tampung = models.CharField(max_length=)
