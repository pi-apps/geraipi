from django.db.models import Avg
from django.urls import reverse
from rest_framework import serializers

from frontend.view_helper import translater
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

# from rest_framework.response import Response
# from .ulasan_serializer import UlasanSerializer


class KategoriSerializer(serializers.HyperlinkedModelSerializer):
    nama = serializers.SerializerMethodField()

    class Meta:
        model = Kategori
        fields = ["url", "kode", "icon", "nama"]

    def get_nama(self, obj):
        user = self.context.get("users", None)
        languanges_code = "id"
        if not user:
            user = None
        elif user.is_anonymous:
            user = None
        else:
            languanges_code = user.languages.code if user.languages else "id"
        translate_text = translater(translate_to=languanges_code, page=obj.nama, values=obj.nama)
        return translate_text


class TipeProdukSerializer(serializers.HyperlinkedModelSerializer):
    nama = serializers.SerializerMethodField()

    class Meta:
        model = TipeProduk
        fields = ["url", "nama"]

    def get_nama(self, obj):
        user = self.context["users"]
        languanges_code = "id"
        if not user.is_authenticated:
            user = None
        elif user.is_anonymous:
            user = None
        else:
            languanges_code = user.languages.code if user.languages else "id"
        translate_text = translater(translate_to=languanges_code, page=obj.nama, values=obj.nama)
        return translate_text


class WarnaProdukSerializer(serializers.HyperlinkedModelSerializer):
    nama = serializers.SerializerMethodField()

    class Meta:
        model = WarnaProduk
        fields = ["url", "nama"]

    def get_nama(self, obj):
        user = self.context.get("users", None)
        languanges_code = "id"
        if not user:
            user = None
        elif user.is_anonymous:
            user = None
        else:
            languanges_code = user.languages.code if user.languages else "id"
        translate_text = translater(translate_to=languanges_code, page=obj.nama, values=obj.nama)
        return translate_text


class GambarProdukSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GambarProduk
        fields = ["gambar", "nama"]


class ProdukSerializer(serializers.HyperlinkedModelSerializer):
    kategori = KategoriSerializer(many=True)
    tipe = TipeProdukSerializer()
    warna = WarnaProdukSerializer(many=True)
    store = serializers.SerializerMethodField()
    gambar = serializers.SerializerMethodField()
    count_star = serializers.SerializerMethodField()
    produk_detail_url = serializers.SerializerMethodField()
    terjual = serializers.SerializerMethodField()

    nama = serializers.SerializerMethodField()

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
            "terjual",
        ]

    def get_nama(self, obj):
        user = self.context.get("users", None)
        user_lang = "id"
        if not user:
            if not user.is_authenticated:
                user = None
            user = None
        elif user.is_anonymous:
            user = None
        else:
            user_lang = user.languages.code if user.languages else "id"
        return translater(translate_to=user_lang, page=obj.nama, values=obj.nama)

    def get_count_star(self, obj):
        countstar = (
            UlasanCart.objects.filter(produkitem_id=obj.id).aggregate(Avg("produk"))["produk__avg"] or 0  # noqa: W503
        )
        return countstar

    def get_produk_detail_url(self, obj):
        urldetail = reverse("produk_detail", kwargs={"slug": obj.slug})
        return urldetail

    def get_gambar(self, obj):
        gambars = GambarProduk.objects.filter(produk__pk=obj.pk, gambar__isnull=False).order_by("-pk")
        return GambarProdukSerializer(gambars, many=True).data

    def get_store(self, obj):
        stores = UserStore.objects.filter(pk=obj.store.id)
        if stores.exists():
            stores = stores.first()
        return UserStoreSerializer(stores).data

    def get_terjual(self, obj):
        terjual = 0
        terjual = UlasanCart.objects.filter(produkitem_id=obj.id).count()
        return terjual
