from django.db import models

from master.models import Distric, Provinsi, Regency, Village

# from django.contrib.auth.models import User
from profiles.models import UserProfile


# Create your models here.
class UserStore(models.Model):
    users = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    nama = models.TextField(null=False, blank=False)
    coin = models.FloatField(default=0)
    deskripsi = models.TextField(null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    telpon = models.CharField(max_length=40, blank=True, null=True)
    is_active_store = models.BooleanField(default=False)
    aggrement = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nama or "-"


class UserStoreAddress(models.Model):
    userstore = models.ForeignKey(
        UserStore, blank=True, null=True, on_delete=models.CASCADE
    )
    address = models.TextField(blank=True, null=True)
    rt = models.CharField(max_length=10, blank=True, null=True)
    rw = models.CharField(max_length=10, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    province = models.ForeignKey(Provinsi, on_delete=models.CASCADE, null=True)
    regency = models.ForeignKey(Regency, on_delete=models.CASCADE, null=True)
    distric = models.ForeignKey(Distric, on_delete=models.CASCADE, null=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return super().__str__()


class UserStoreWdHistory(models.Model):
    userstore = models.ForeignKey(UserStore, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_created=True, auto_now=True)
    jumlah = models.FloatField(default=0)

    def __str__(self):
        return self.date


class UserNotification(models.Model):
    notificationfor = models.ForeignKey(
        UserProfile, null=True, on_delete=models.CASCADE
    )
    notificationfrom = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self) -> str:
        return self.notificationfrom or "-"


class Expedisi(models.Model):
    SOURCE_REQUEST = [
        (1, "Raja Ongkir"),
        (2, "Biteship"),
    ]
    code = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255)
    url_request = models.URLField(null=True, blank=True)
    source_request = models.IntegerField(choices=SOURCE_REQUEST, default=1)

    def __str__(self):
        return self.nama
