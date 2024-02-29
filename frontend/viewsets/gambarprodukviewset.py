from rest_framework import viewsets

from frontend.serializers import GambarProdukSerializer
from produk.models import GambarProduk


class GambarProdukViewSet(viewsets.ModelViewSet):
    queryset = GambarProduk.objects.all()
    serializer_class = GambarProdukSerializer
