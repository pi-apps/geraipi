import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django_resized import ResizedImageField

from master.models import Country, Distric, Provinsi, Regency, Village
from profiles.models import LangSupport, UserProfile
from store.models import Expedisi, UserStore


# Create your models here.
class Kategori(models.Model):
    kode = models.CharField(unique=True, max_length=255)
    icon = models.FileField(upload_to="icon_kategori")
    nama = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self) -> str:
        return self.kode


class TipeProduk(models.Model):
    nama = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self) -> str:
        return self.nama


class WarnaProduk(models.Model):
    nama = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.nama


class Produk(models.Model):
    store = models.ForeignKey(UserStore, on_delete=models.CASCADE)

    nama = models.TextField(null=True, blank=True)
    harga = models.FloatField(null=True, blank=True)
    kategori = models.ManyToManyField(Kategori)
    detail = models.TextField(null=True, blank=True)

    tipe = models.ForeignKey(
        TipeProduk, blank=True, null=True, on_delete=models.CASCADE
    )
    warna = models.ManyToManyField(WarnaProduk, blank=True)
    stok_produk = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    stok = models.IntegerField(default=0)
    is_promo = models.IntegerField(default=False)

    negara = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    descriptis_langs = models.JSONField(null=True)

    is_archive = models.BooleanField(default=False)

    berat = models.FloatField(default=0)
    lebar = models.FloatField(default=0)

    slug = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    cross_boarder = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nama

    @property
    def gambarutama(self):
        return self.gambarproduk_set.first()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nama)
        super().save(*args, **kwargs)


class GambarProduk(models.Model):
    sortings = models.IntegerField(default=0)
    produk = models.ForeignKey(Produk, null=True, on_delete=models.CASCADE)
    gambar = ResizedImageField(
        force_format="WEBP", quality=75, upload_to="produk_image/"
    )
    nama = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.nama or "-"


class ProdukStok(models.Model):
    store = models.ForeignKey(UserStore, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class ProdukTransaksi(models.Model):
    JENIS = [(1, "Stok awal"), (2, "Stok tambahan")]

    kode_transaksi = models.CharField(max_length=255)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jenis = models.IntegerField(default=1, choices=JENIS)
    date_in = models.DateTimeField(auto_created=True)
    date_out = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.kode_transaksi


class Cart(models.Model):
    STATUS = [(1, "Pending"), (2, "Diproses"), (3, "Selesai"), (4, "Confirm")]

    STATUS_TOKO = [(1, "Pending"), (2, "Diproses"), (3, "Dikirim"), (4, "Confirm")]

    kode = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.IntegerField(default=1, choices=STATUS)
    tanggal_dikirim = models.DateTimeField(null=True, blank=True)
    tanggal_selesai = models.DateTimeField(null=True, blank=True)
    status_pembayaran = models.IntegerField(default=1, choices=STATUS)
    status_toko = models.IntegerField(
        default=0, choices=STATUS_TOKO, blank=True, null=True
    )
    nomor_resi = models.CharField(blank=True, null=True, max_length=255)
    catatan = models.TextField(blank=True, null=True, max_length=255)
    expedisi = models.ForeignKey(
        Expedisi, blank=True, null=True, on_delete=models.CASCADE
    )
    tanggal = models.DateTimeField(auto_created=True, blank=True, null=True)

    def __str__(self):
        return self.kode

    def save(self, *args, **kwargs):
        if not self.kode:
            self.kode = uuid.uuid4().hex.upper()[0:6]
        return super().save(*args, **kwargs)


class UlasanCart(models.Model):
    cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE)
    produkitem = models.ForeignKey(
        Produk, blank=True, null=True, on_delete=models.CASCADE
    )
    pengiriman = models.FloatField(default=0)
    produk = models.FloatField(default=0)
    catatan = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.catatan


class ProdukChartItem(models.Model):
    store = models.ForeignKey(UserStore, on_delete=models.CASCADE)
    nama = models.TextField(null=True, blank=True)
    harga = models.FloatField(null=True, blank=True)
    kategori = models.ManyToManyField(Kategori)
    detail = models.TextField(null=True, blank=True)
    tipe = models.ForeignKey(
        TipeProduk, blank=True, null=True, on_delete=models.CASCADE
    )
    warna = models.ManyToManyField(WarnaProduk, blank=True)
    stok_produk = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    stok = models.IntegerField(default=0)
    is_promo = models.IntegerField(default=False)
    berat = models.FloatField(default=0)
    lebar = models.FloatField(default=0)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


class UserCartItem(models.Model):
    TYPE = [
        (1, "Domestic"),
        (2, "Overseas"),
    ]
    wallet = models.CharField(max_length=255, null=True, blank=True)
    no_telepon = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=4, blank=True, null=True, default="ID")
    typeuser = models.IntegerField(choices=TYPE, default=1)
    token = models.TextField(blank=True, null=True)


class AddressUserChartItem(models.Model):
    TYPE = [
        (1, "Domestic"),
        (2, "Overseas"),
    ]
    userprofile = models.ForeignKey(
        UserCartItem, on_delete=models.CASCADE, null=True, blank=True
    )
    typeaddress = models.IntegerField(choices=TYPE, default=1)

    name = models.CharField(max_length=255)
    address = models.TextField()
    zipcode = models.CharField(max_length=255, default="-")
    is_primary = models.BooleanField(default=False)

    province = models.ForeignKey(Provinsi, on_delete=models.CASCADE, null=True)
    regency = models.ForeignKey(Regency, on_delete=models.CASCADE, null=True)
    distric = models.ForeignKey(Distric, on_delete=models.CASCADE, null=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
    rt = models.CharField(max_length=5, blank=True, null=True)
    rw = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.address


class StoreCartItem(models.Model):
    users = models.ForeignKey(UserCartItem, on_delete=models.CASCADE)
    nama = models.TextField(null=False, blank=False)
    coin = models.FloatField(null=True, blank=True, default=0)
    deskripsi = models.TextField(null=True, blank=True)


class StoreAddressCartItem(models.Model):
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


class CartItem(models.Model):
    unique_cart = models.CharField(max_length=50)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    jumlah = models.IntegerField(default=1)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    produk_chart = models.ForeignKey(
        ProdukChartItem, blank=True, null=True, on_delete=models.CASCADE
    )
    user_chart = models.ForeignKey(
        UserCartItem, blank=True, null=True, on_delete=models.CASCADE
    )
    store_chart = models.ForeignKey(
        StoreCartItem, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return " cart " + self.unique_cart


class DeskripsiProduk(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    languange = models.ForeignKey(LangSupport, on_delete=models.CASCADE)
    deskripsi = models.TextField(blank=True, null=True)
