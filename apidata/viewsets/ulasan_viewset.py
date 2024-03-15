from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apidata.serializers.ulasan_serializer import UlasanSerializer
from produk.models import UlasanCart


class UlasanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = UlasanCart.objects.all().order_by("-pk")
    serializer_class = UlasanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["produkitem__id"]
    # pagination_class = None
    http_method_names = ["get", "head"]
