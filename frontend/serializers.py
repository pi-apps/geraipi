from rest_framework import serializers

from master.models.distric import Distric
from master.models.provinsi import Provinsi
from master.models.regency import Regency
from master.models.village import Village
from produk.models import GambarProduk, Kategori, Produk
from profiles.models import UserProfile, UserProfileAddress


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["url", "username", "email", "is_staff"]


class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = "__all__"


class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = [
            "url",
            "nama",
            "harga",
            "kategori",
            "detail",
            "tipe",
            "warna",
            "stok_produk",
            "slug",
            "store",
        ]


class GambarProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = GambarProduk
        fields = "__all__"


class ProvinsiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provinsi
        fields = "__all__"


class RegencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Regency
        fields = "__all__"


class DistricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distric
        fields = "__all__"


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileAddress
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
