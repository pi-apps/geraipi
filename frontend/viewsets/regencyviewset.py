from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from frontend.serializers import RegencySerializer
from master.models.regency import Regency


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
