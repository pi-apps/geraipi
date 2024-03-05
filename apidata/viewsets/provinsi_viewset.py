from rest_framework import viewsets, filters

from apidata.serializers.provinsi_serializer import ProvinsiSerializer
from django_filters.rest_framework import DjangoFilterBackend
from master.models import Provinsi


class ProvinsiViewSet(viewsets.ModelViewSet):
    queryset = Provinsi.objects.all()
    serializer_class = ProvinsiSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["code", "nama"]
    search_fields = ["code", "nama"]
    http_method_names = ["get", "head"]
