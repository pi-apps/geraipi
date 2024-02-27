from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from django.db.models import Avg
from apidata.serializers.produks_serializer import (
    ProdukSerializer,
    TipeProdukSerializer,
    KategoriSerializer,
    WarnaProdukSerializer,
    GambarProdukSerializer
)
from produk.models import Produk, TipeProduk, Kategori, WarnaProduk, GambarProduk
from django_filters.rest_framework import DjangoFilterBackend


class KategoriViewset(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    http_method_names = ['get', 'head', 'option']


class TipeProdukViewset(viewsets.ModelViewSet):
    queryset = TipeProduk.objects.all()
    serializer_class = TipeProdukSerializer
    http_method_names = ['get', 'head', 'option']


class WarnaProdukViewset(viewsets.ModelViewSet):
    queryset = WarnaProduk.objects.all()
    serializer_class = WarnaProdukSerializer
    http_method_names = ['get', 'head', 'option']


class GambarProdukViewset(viewsets.ModelViewSet):
    queryset = GambarProduk.objects.all()
    serializer_class = GambarProdukSerializer
    http_method_names = ['get', 'head', 'option']


class ProdukViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategori']
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    http_method_names = ['get', 'head', 'option']
