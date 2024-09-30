from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apidata.serializers.regency_serializer import RegencySerializer
from master.models.regency import Regency


class RegencyViewSet(viewsets.ModelViewSet):
    queryset = Regency.objects.all()
    serializer_class = RegencySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["code", "province_code", "name"]
    search_fields = ["code", "name"]
    http_method_names = ["get", "head"]
