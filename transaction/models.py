import uuid

from django.db import models
from django.utils import timezone

from master.models.country import Country
from master.models.distric import Distric
from master.models.expedisi import Expedisi
from master.models.provinsi import Provinsi
from master.models.regency import Regency
from master.models.village import Village
from produk.models import Produk
from profiles.models import LangSupport, UserProfile
from store.models import UserStore

TYPE = [
    (1, "Domestic"),
    (2, "Overseas"),
]


class TransactionUser(models.Model):
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    image_profile = models.ImageField(upload_to="transaction_profile_img/", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    wallet = models.CharField(max_length=255, null=True, blank=True)
    no_telepon = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=4, blank=True, null=True, default="ID")
    languages = models.ForeignKey(LangSupport, blank=True, null=True, on_delete=models.SET_NULL)
    typeuser = models.IntegerField(choices=TYPE, default=1)
    coin = models.FloatField(default=0)
    fcm_token = models.TextField(null=True, blank=True)


class Cart(models.Model):
    STATUS = [(1, "Pending"), (2, "Diproses"), (3, "Selesai"), (4, "Confirm")]
    STATUS_TOKO = [(1, "Pending"), (2, "Diproses"), (3, "Dikirim"), (4, "Confirm")]

    kode = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(TransactionUser, on_delete=models.CASCADE, related_name="cart_user")
    status = models.IntegerField(default=1, choices=STATUS)
    tanggal_dikirim = models.DateTimeField(null=True, blank=True)
    tanggal_selesai = models.DateTimeField(null=True, blank=True)
    status_pembayaran = models.IntegerField(default=1, choices=STATUS)
    status_toko = models.IntegerField(default=0, choices=STATUS_TOKO, blank=True, null=True)
    nomor_resi = models.CharField(blank=True, null=True, max_length=255)
    catatan = models.TextField(blank=True, null=True, max_length=255)
    expedisi = models.ForeignKey(
        Expedisi, blank=True, null=True, on_delete=models.CASCADE, related_name="cart_expedisi"
    )
    tanggal = models.DateTimeField(auto_created=True, blank=True, null=True)

    def __str__(self):
        return self.kode

    @property
    def ulasans(self):
        ulasan = UlasanCart.objects.filter(cart_id=self.id).first()
        return ulasan

    def save(self, *args, **kwargs):
        if not self.kode:
            self.kode = uuid.uuid4().hex.upper()[0:6]
        return super().save(*args, **kwargs)


class CartProdukKategori(models.Model):
    kode = models.CharField(unique=True, max_length=255)
    icon = models.FileField(upload_to="icon_kategori")
    nama = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self) -> str:
        return self.kode


class CartProdukTipe(models.Model):
    nama = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self) -> str:
        return self.nama


class CartProdukWarna(models.Model):
    nama = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.nama


class TransactionUserStore(models.Model):
    users = models.ForeignKey(TransactionUser, on_delete=models.CASCADE, related_name="transaction_user_store")
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


class CartProduk(models.Model):
    store = models.ForeignKey(TransactionUserStore, on_delete=models.CASCADE)

    nama = models.TextField(null=True, blank=True)
    harga = models.FloatField(null=True, blank=True)
    kategori = models.ManyToManyField(CartProdukKategori)
    detail = models.TextField(null=True, blank=True)

    tipe = models.ForeignKey(CartProdukTipe, blank=True, null=True, on_delete=models.CASCADE)
    warna = models.ManyToManyField(CartProdukWarna, blank=True, related_name="cart_produk_warna")
    stok_produk = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    stok = models.IntegerField(default=0)
    is_promo = models.IntegerField(default=False)

    negara = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.CASCADE, related_name="cart_produk_negara"
    )
    descriptis_langs = models.JSONField(null=True)

    is_archive = models.BooleanField(default=False)

    berat = models.FloatField(default=0)
    lebar = models.FloatField(default=0)

    slug = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    cross_boarder = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nama


class CartItem(models.Model):
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

    def __str__(self):
        return str(self.id)


class UlasanCart(models.Model):
    cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE)
    produkitem = models.ForeignKey(
        Produk, blank=True, null=True, on_delete=models.CASCADE, related_name="ulasan_produk"
    )
    pengiriman = models.FloatField(default=0)
    produk = models.FloatField(default=0)
    catatan = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.catatan


class AddressUserChart(models.Model):
    TYPE = [
        (1, "Domestic"),
        (2, "Overseas"),
    ]
    userprofile = models.ForeignKey(CartItem, on_delete=models.CASCADE, null=True, blank=True)
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


class ReportImage(models.Model):
    image = models.ImageField(blank=False, null=False)

    def __str__(self):
        return str(self.id)


class Report(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vendor = models.ForeignKey(UserStore, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    # image = models.ManyToManyField(ReportImage)
    catatan = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.user
