from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from frontend.serializers import ProvinsiSerializer
from master.models.provinsi import Provinsi


class ProvinsiViewset(viewsets.ModelViewSet):
    queryset = Provinsi.objects.all()
    serializer_class = ProvinsiSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["code", "nama"]
    filterset_fields = ["nama"]
