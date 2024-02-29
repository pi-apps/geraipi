from frontend import viewsets
from frontend.serializers import KategoriSerializer
from produk.models import Kategori


class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
