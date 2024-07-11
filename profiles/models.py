from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField

from master.models import Distric, Provinsi, Regency, Village
from profiles.helper import get_random

from .managers import UserManager

TYPE = [
    (1, "Domestic"),
    (2, "Overseas"),
]


class LangSupport(models.Model):
    code = models.CharField(blank=True, null=True, max_length=255)
    alias = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_active_store = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Language"

    def __str__(self):
        return self.alias or "-"


class UserProfile(AbstractUser):
    image_profile = ResizedImageField(
        force_format="WEBP", quality=75, upload_to="profile_img/", blank=True, null=True
    )
    wallet = models.CharField(max_length=255, null=True, blank=True)
    no_telepon = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=4, blank=True, null=True, default="ID")
    languages = models.ForeignKey(
        LangSupport, blank=True, null=True, on_delete=models.SET_NULL
    )
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

    province = models.ForeignKey(
        Provinsi, on_delete=models.CASCADE, null=True, blank=True
    )
    regency = models.ForeignKey(
        Regency, on_delete=models.CASCADE, null=True, blank=True
    )
    distric = models.ForeignKey(
        Distric, on_delete=models.CASCADE, null=True, blank=True
    )
    village = models.ForeignKey(
        Village, on_delete=models.CASCADE, null=True, blank=True
    )
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
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, blank=True, null=True
    )
    jumlah = models.FloatField(default=0)
    tanggal = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self) -> str:
        return str(self.jumlah)


class UserwithdrawlTransactionRequest(models.Model):
    REQUEST_STATUS = ((1, "Request User"), (2, "Selesai Diproses"))
    kode = models.CharField(max_length=255, default=get_random())
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, blank=True, null=True
    )
    jumlah = models.FloatField(default=0.0)
    tanggal = models.DateTimeField(auto_now=True, auto_created=True)
    status = models.IntegerField(choices=REQUEST_STATUS, blank=True, null=True)

    def __str__(self):
        return str(self.kode)
    
class UserAppliedMember(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(blank=False, max_length=255)
    email = models.EmailField(blank=True, null=True)
    nomor = models.CharField(blank=True, null=True, max_length=255)
    tanggal = models.DateTimeField(auto_now=True, auto_created=True)
    is_accept = models.BooleanField(default=False)
    accept_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    
    def save(self, *args, **kwargs):
       if self.is_accept:
           self.create_generator()
       super(UserAppliedMember, self).save(*args, **kwargs) # Call the real save() method
    
    def create_generator(self):
        usergenerator = UserCodeGenerator()
        usergenerator.code = get_random()
        usergenerator.user = self.user
        usergenerator.user_apply_id = self.pk
        usergenerator.quota_withdrawl = 5
        usergenerator.bypass_waiting = True
        usergenerator.updated_information = True
        usergenerator.is_active = True
        usergenerator.save()

class UserCodeGenerator(models.Model):
    user_apply = models.ForeignKey(UserAppliedMember, on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=50)
    quota_withdrawl = models.IntegerField(default=0)
    bypass_waiting = models.BooleanField(default=False)
    updated_information = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        super(UserCodeGenerator, self).save(*args, **kwargs)

class UserSettingsMember(models.Model):
    code = models.CharField(blank=True, null=True, max_length=50)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    quota_withdrawl = models.IntegerField(default=0)
    bypass_waiting = models.BooleanField(default=False)
    updated_information = models.BooleanField(default=False)
