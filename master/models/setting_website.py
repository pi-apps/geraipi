from django.db import models


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
