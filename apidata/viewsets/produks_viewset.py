from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apidata.serializers.produks_serializer import (
    GambarProdukSerializer,
    KategoriSerializer,
    ProdukSerializer,
    TipeProdukSerializer,
    WarnaProdukSerializer,
)
from produk.models import GambarProduk, Kategori, Produk, TipeProduk, WarnaProduk


class KategoriViewset(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    http_method_names = ["get", "head", "option"]


class TipeProdukViewset(viewsets.ModelViewSet):
    queryset = TipeProduk.objects.all()
    serializer_class = TipeProdukSerializer
    http_method_names = ["get", "head", "option"]


class WarnaProdukViewset(viewsets.ModelViewSet):
    queryset = WarnaProduk.objects.all()
    serializer_class = WarnaProdukSerializer
    http_method_names = ["get", "head", "option"]


class GambarProdukViewset(viewsets.ModelViewSet):
    queryset = GambarProduk.objects.all()
    serializer_class = GambarProdukSerializer
    http_method_names = ["get", "head", "option"]


class ProdukViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["kategori", "negara", "slug"]
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    http_method_names = ["get", "head", "option"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["users"] = self.request.user
        return context
