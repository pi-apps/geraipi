from rest_framework import viewsets, filters

from apidata.serializers.regency_serializer import RegencySerializer
from django_filters.rest_framework import DjangoFilterBackend
from master.models import Regency


class RegencyViewSet(viewsets.ModelViewSet):
    queryset = Regency.objects.all()
    serializer_class = RegencySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["code", "province_code", "name"]
    search_fields = ["code", "province_code", "name"]
    http_method_names = ["get", "head"]
