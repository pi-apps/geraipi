from profiles.models import UserProfile
from produk.models import Produk, Kategori, GambarProduk
from master.models import Provinsi, Distric, Regency, Village
from rest_framework import viewsets, filters
from frontend.serializers import UserSerializer, ProdukSerializer, KategoriSerializer, GambarProdukSerializer, ProvinsiSerializer, DistricSerializer, RegencySerializer, VillageSerializer, UserProfileSerializer, UserAddressSerializer
from profiles.models import UserProfile, UserProfileAddress
from django_filters.rest_framework import DjangoFilterBackend


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
    filterset_fields = ['kategori']
    ordering_fields = ['harga', 'stok']

    def get_queryset(self):
        queryset = self.queryset
        kategoris = self.request.GET.get('kategori')
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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['code', 'nama']
    filterset_fields = ['nama']

class RegencyViewset(viewsets.ModelViewSet):
    queryset = Regency.objects.all()
    serializer_class = RegencySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['province_code']

class DistricViewset(viewsets.ModelViewSet):
    queryset = Distric.objects.all()
    serializer_class = DistricSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['regency_code']

class VillagerViewset(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer

class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserAddressViewset(viewsets.ModelViewSet):
    queryset = UserProfileAddress.objects.all()
    serializer_class = UserAddressSerializer
