from django.db import models
from solo.models import SingletonModel


class ConfigurationWebsite(SingletonModel):
    api_key_pi = models.CharField(blank=True, null=True, max_length=255)
    wallet_private_pi = models.CharField(blank=True, null=True, max_length=255)
    pajak_beli = models.FloatField(default=0)
    pajak_withdrawl = models.FloatField(default=0)
    koin_website = models.FloatField(default=0)
    konfigurasi_firebase = models.FileField(blank=True, null=True, upload_to="konfigurasi/")
    url_check_resi = models.URLField(blank=True, null=True)
    api_check_resi = models.CharField(blank=True, null=True, max_length=200)
    video_splash = models.FileField(blank=True, null=True, upload_to="splash", unique=True)

    api_biteship = models.CharField(blank=True, null=True, max_length=255)
    verification = models.CharField(blank=True, null=True, max_length=255)
    bypass_expedisi = models.BooleanField(default=False)