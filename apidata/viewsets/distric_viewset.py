from rest_framework import viewsets, filters

from apidata.serializers.distric_serializer import DistricSerializer
from django_filters.rest_framework import DjangoFilterBackend
from master.models import Distric


class DistricViewSet(viewsets.ModelViewSet):
    queryset = Distric.objects.all()
    serializer_class = DistricSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["code", "regency_code", "name"]
    search_fields = ["code", "regency_code", "name"]
    http_method_names = ["get", "head"]
