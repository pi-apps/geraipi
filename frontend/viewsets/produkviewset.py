from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from frontend.serializers import ProdukSerializer
from produk.models import Produk


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
