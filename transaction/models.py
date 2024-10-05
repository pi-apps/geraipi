import uuid
from django.db import models
from profiles.models import UserProfile, LangSupport
from store.models import UserStore
from master.models.provinsi import Provinsi
from master.models.regency import Regency
from master.models.distric import Distric
from master.models.village import Village
from master.models.country import Country
from produk.models import Produk
from django.utils import timezone

from transaction.utils import TYPE, TYPE_CART_ITEM, STATUS, STATUS_TOKO
from master.utils import SOURCE_REQUEST

# Creating Backup User
class TransactionUser(models.Model):
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name="transaction_origin_user_cart")
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


# Creating Backup Store
class TransactionUserStore(models.Model):
    store = models.ForeignKey(UserStore, on_delete=models.SET_NULL, null=True, related_name="transaction_transactionuserstore_store")
    users = models.ForeignKey(TransactionUser, on_delete=models.SET_NULL, null=True, related_name="transaction_user_store")
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


# Creating Addres for user
class AddressUserChart(models.Model):
    user = models.ForeignKey(TransactionUser, on_delete=models.CASCADE, null=True, blank=True, related_name="transaction_addressuserchart_user")
    typeaddress = models.IntegerField(choices=TYPE_CART_ITEM, default=1)

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
    

# Creating Backup Produk Katgori
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


class CartProduk(models.Model):
    store = models.ForeignKey(TransactionUserStore, null=True, on_delete=models.SET_NULL, related_name="transaction_cartproduk_store")
    produk = models.ForeignKey(Produk, null=True, on_delete=models.SET_NULL, related_name="transaction_cartproduk_produk")

    nama = models.TextField(null=True, blank=True)
    harga = models.FloatField(null=True, blank=True)
    kategori = models.ManyToManyField(CartProdukKategori)
    detail = models.TextField(null=True, blank=True)

    tipe = models.ForeignKey(CartProdukTipe, blank=True, null=True, on_delete=models.SET_NULL, related_name="transaction_cartproduk_tipe")
    warna = models.ManyToManyField(CartProdukWarna, blank=True, null=True, related_name="transaction_cartproduk_warna")
    stok_produk = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    stok = models.IntegerField(default=0)
    is_promo = models.IntegerField(default=False)

    negara = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.CASCADE, related_name="transaction_cartproduk_negara"
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


class CartExpedisi(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    nama = models.CharField(max_length=255)
    url_request = models.URLField(null=True, blank=True)
    source_request = models.IntegerField(choices=SOURCE_REQUEST, default=1)

    def __str__(self):
        return self.nama


class Cart(models.Model):
    kode = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(TransactionUser, on_delete=models.CASCADE, related_name="transaction_cart_user")
    status = models.IntegerField(default=1, choices=STATUS)
    tanggal_dikirim = models.DateTimeField(null=True, blank=True)
    tanggal_selesai = models.DateTimeField(null=True, blank=True)
    status_pembayaran = models.IntegerField(default=1, choices=STATUS)
    status_toko = models.IntegerField(default=0, choices=STATUS_TOKO, blank=True, null=True)
    nomor_resi = models.CharField(blank=True, null=True, max_length=255)
    catatan = models.TextField(blank=True, null=True, max_length=255)
    expedisi = models.ForeignKey(
        CartExpedisi, blank=True, null=True, on_delete=models.CASCADE, related_name="transaction_cart_expedisi"
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


class CartItem(models.Model):
    unique_cart = models.CharField(max_length=50, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, related_name="transaction_cartitem_cart")
    jumlah = models.IntegerField(default=1)
    produk = models.ForeignKey(CartProduk, null=True, on_delete=models.SET_NULL, related_name="transaction_cartitem_produk")
    user_chart = models.ForeignKey(TransactionUser, blank=True, null=True, on_delete=models.SET_NULL, related_name="transaction_cartitem_user_chart")
    store_chart = models.ForeignKey(TransactionUserStore, blank=True, null=True, on_delete=models.SET_NULL, related_name="transaction_cartitem_store_chart")

    def __str__(self):
        return " cart " + self.unique_cart


class UlasanCart(models.Model):
    cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name="transaction_ulasancart_cart")
    origin_produk = models.ForeignKey(
        CartProduk, blank=True, null=True, on_delete=models.CASCADE, related_name="transaction_ulasancart_produk"
    )
    pengiriman = models.FloatField(default=0)
    produk = models.FloatField(default=0)
    catatan = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.catatan


class ReportImage(models.Model):
    image = models.ImageField(blank=False, null=False)

    def __str__(self):
        return str(self.id)


class Report(models.Model):
    user = models.ForeignKey(TransactionUser, on_delete=models.CASCADE, related_name="transaction_report_user")
    vendor = models.ForeignKey(TransactionUserStore, on_delete=models.CASCADE, related_name="transaction_report_vendor")
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name="transaction_report_cart_item")
    image = models.ManyToManyField(ReportImage, related_name="transaction_report_images")
    catatan = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.user
