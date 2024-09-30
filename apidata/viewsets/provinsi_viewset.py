from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apidata.serializers.provinsi_serializer import ProvinsiSerializer
from master.models.provinsi import Provinsi


class ProvinsiViewSet(viewsets.ModelViewSet):
    queryset = Provinsi.objects.all()
    serializer_class = ProvinsiSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["code", "nama"]
    search_fields = ["code", "nama"]
    http_method_names = ["get", "head"]
