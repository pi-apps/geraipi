from django.db.models import Avg
from django.urls import reverse
from rest_framework import serializers

from produk.models import (
    GambarProduk,
    Kategori,
    Produk,
    TipeProduk,
    UlasanCart,
    WarnaProduk,
)
from store.models import UserStore

from .stores_serializer import UserStoreSerializer


class KategoriSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kategori
        fields = ["url", "kode", "icon", "nama"]


class TipeProdukSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipeProduk
        fields = ["url", "nama"]


class WarnaProdukSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WarnaProduk
        fields = ["url", "nama"]


class GambarProdukSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GambarProduk
        fields = ["gambar", "nama"]


class ProdukSerializer(serializers.HyperlinkedModelSerializer):
    kategori = KategoriSerializer(many=True)
    tipe = TipeProdukSerializer(many=True)
    warna = WarnaProdukSerializer(many=True)
    store = serializers.SerializerMethodField()
    gambar = serializers.SerializerMethodField()
    count_star = serializers.SerializerMethodField()
    produk_detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Produk
        fields = [
            "id",
            "url",
            "nama",
            "harga",
            "kategori",
            "tipe",
            "warna",
            "gambar",
            "detail",
            "stok_produk",
            "stok",
            "is_promo",
            "berat",
            "lebar",
            "slug",
            "created_at",
            "store",
            "count_star",
            "produk_detail_url",
        ]

    def get_count_star(self, obj):
        countstar = (
            UlasanCart.objects.filter(produkitem_id=obj.id).aggregate(Avg("produk"))[
                "produk__avg"
            ]
            or 0  # noqa: W503
        )
        return countstar

    def get_produk_detail_url(self, obj):
        urldetail = reverse("detail_produk", kwargs={"slug": obj.slug})
        return urldetail

    def get_gambar(self, obj):
        gambars = GambarProduk.objects.filter(produk__pk=obj.pk).order_by("-pk")
        return GambarProdukSerializer(gambars, many=True).data

    def get_store(self, obj):
        stores = UserStore.objects.filter(pk=obj.store.id)
        if stores.exists():
            stores = stores.first()
        return UserStoreSerializer(stores).data
