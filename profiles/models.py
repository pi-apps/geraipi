from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from master.models import Provinsi, Regency, Distric, Village
from django_resized import ResizedImageField

from .managers import UserManager

TYPE = [
    (1, "Domestic"),
    (2, "Overseas"),
]

class LangSupport(models.Model):
    code = models.CharField(blank=True, null=True, max_length=255)
    alias = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Language"

    def __str__(self):
        return self.alias or "-"

class UserProfile(AbstractUser):
    image_profile = ResizedImageField(force_format="WEBP", quality=75, upload_to="profile_img/", blank=True, null=True)
    wallet = models.CharField(max_length=255, null=True, blank=True)
    no_telepon = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=4, blank=True, null=True, default="ID")
    languages = models.ForeignKey(LangSupport, blank=True, null=True, on_delete=models.SET_NULL)
    typeuser = models.IntegerField(choices=TYPE, default=1)
    coin = models.FloatField(default=0)
    fcm_token = models.TextField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return self.nama or "-"


class UserProfileAddress(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    typeaddress = models.IntegerField(choices=TYPE, default=1)

    name = models.CharField(max_length=255)
    address = models.TextField()
    zipcode = models.CharField(max_length=255, default="-")
    is_primary = models.BooleanField(default=False)

    province = models.ForeignKey(Provinsi, on_delete=models.CASCADE, null=True, blank=True)
    regency = models.ForeignKey(Regency, on_delete=models.CASCADE, null=True, blank=True)
    distric = models.ForeignKey(Distric, on_delete=models.CASCADE, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True)
    rt = models.CharField(max_length=5, blank=True, null=True)
    rw = models.CharField(max_length=5, blank=True, null=True)
    
    class Meta:
        verbose_name = "UserProfileAddress"
        verbose_name_plural = "UserProfileAddresss"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("UserProfileAddress_detail", kwargs={"pk": self.pk})


class UserWithdrawlTransaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    jumlah = models.FloatField(default=0)
    tanggal = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self) -> str:
        return str(self.jumlah)
    
class UserwithdrawlTransactionRequest(models.Model):
    REQUEST_STATUS = (
        (1, "Request User"),
        (2, "Selesai Diproses")
    )
    kode = models.CharField(blank=True, null=True, max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    jumlah = models.FloatField(default=0.0)
    tanggal = models.DateTimeField(auto_now=True, auto_created=True)
    status = models.IntegerField(choices=REQUEST_STATUS, blank=True, null=True)
    
    def __str__(self):
        return str(self.kode)
