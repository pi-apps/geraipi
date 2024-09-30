from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apidata.serializers.distric_serializer import DistricSerializer
from master.models.distric import Distric


class DistricViewSet(viewsets.ModelViewSet):
    queryset = Distric.objects.all()
    serializer_class = DistricSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["code", "regency_code", "name"]
    search_fields = ["code", "regency_code", "name"]
    http_method_names = ["get", "head"]
