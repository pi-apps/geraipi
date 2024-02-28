from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from frontend.serializers import (
    DistricSerializer,
    GambarProdukSerializer,
    KategoriSerializer,
    ProdukSerializer,
    ProvinsiSerializer,
    RegencySerializer,
    UserAddressSerializer,
    UserProfileSerializer,
    UserSerializer,
    VillageSerializer,
)
from master.models import Distric, Provinsi, Regency, Village
from produk.models import GambarProduk, Kategori, Produk
from profiles.models import UserProfile, UserProfileAddress


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer


class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["kategori"]
    ordering_fields = ["harga", "stok"]

    def get_queryset(self):
        queryset = self.queryset
        kategoris = self.request.GET.get("kategori")
        if kategoris:
            queryset = queryset.filter(kategori__in=kategoris)
        print(kategoris)
        return queryset


class GambarProdukViewSet(viewsets.ModelViewSet):
    queryset = GambarProduk.objects.all()
    serializer_class = GambarProdukSerializer


class ProvinsiViewset(viewsets.ModelViewSet):
    queryset = Provinsi.objects.all()
    serializer_class = ProvinsiSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["code", "nama"]
    filterset_fields = ["nama"]


class RegencyViewset(viewsets.ModelViewSet):
    queryset = Regency.objects.all()
    serializer_class = RegencySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["code", "name"]
    filterset_fields = ["province_code"]


class DistricViewset(viewsets.ModelViewSet):
    queryset = Distric.objects.all()
    serializer_class = DistricSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["code", "name"]
    filterset_fields = ["regency_code"]


class VillagerViewset(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserAddressViewset(viewsets.ModelViewSet):
    queryset = UserProfileAddress.objects.all()
    serializer_class = UserAddressSerializer
