from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from produk.models import (
    Cart,
    CartItem,
    GambarProduk,
    Kategori,
    Produk,
    ProdukChartItem,
    ProdukStok,
    TipeProduk,
    WarnaProduk,
)

from .forms import CartForm

title = "Gerai PI Admin"
admin.site.site_title = title
admin.site.site_header = title


# Register your models here.
class KategoriAdmin(admin.ModelAdmin):
    list_display = ("kode", "icon", "nama")


admin.site.register(Kategori, KategoriAdmin)

admin.site.register(ProdukChartItem)


class ProdukAdmin(admin.ModelAdmin):
    list_display = ("store", "nama", "detail", "harga")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query = super().get_queryset(request)
        if not request.user.is_superuser:
            if "Toko" in [a.name for a in request.user.groups.all()]:
                query = query.filter(store__users_id=request.user.id)
        elif request.user.is_superuser:
            query = query
        else:
            query = query.none()
        return query


admin.site.register(Produk, ProdukAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ("kode_cart", "user", "status")
    form = CartForm

    def kode_cart(self, obj):
        if obj.kode:
            return obj.kode
        else:
            return "---"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query = super().get_queryset(request)
        if not request.user.is_superuser:
            if "Toko" in [a.name for a in request.user.groups.all()]:
                query = query.filter(user_id=request.user.id)
        elif request.user.is_superuser:
            query = query
        else:
            query = query.none()
        return query


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "get_produk_nama",
        "jumlah",
        "get_status_user",
        "get_status_toko",
        "get_nomor_resi",
        "get_catatan",
    ]

    def get_produk_nama(self, obj):
        produk = None
        if obj.produk:
            produk = obj.produk.nama
        return produk

    get_produk_nama.short_description = "Nama Produk"

    def get_status_user(self, obj):
        statuss = obj.cart.STATUS
        for a in statuss:
            if a[0] == obj.cart.status:
                return a[1]
        return None

    get_status_user.short_description = "Status Pembayaran User"

    def get_status_toko(self, obj):
        statuss = obj.cart.STATUS_TOKO
        for a in statuss:
            if a[0] == obj.cart.status_toko:
                return a[1]
        return None

    get_status_toko.short_description = "Status Toko"

    def get_nomor_resi(self, obj):
        return obj.cart.nomor_resi

    get_nomor_resi.short_description = "Nomor Resi"

    def get_catatan(self, obj):
        return obj.cart.catatan

    get_catatan.short_description = "Catatan"

    def kode_cart(self, obj):
        if obj.kode:
            return obj.kode
        else:
            return "---"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query = super().get_queryset(request)
        if not request.user.is_superuser:
            if "Toko" in [a.name for a in request.user.groups.all()]:
                query = query.filter(cart__user_id=request.user.id)
        elif request.user.is_superuser:
            query = query
        else:
            query = query.none()
        return query


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(TipeProduk)
admin.site.register(WarnaProduk)
admin.site.register(ProdukStok)
admin.site.register(GambarProduk)
