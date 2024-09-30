from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from frontend.serializers import DistricSerializer
from master.models.distric import Distric


class DistricViewset(viewsets.ModelViewSet):
    queryset = Distric.objects.all()
    serializer_class = DistricSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["code", "name"]
    filterset_fields = ["regency_code"]
