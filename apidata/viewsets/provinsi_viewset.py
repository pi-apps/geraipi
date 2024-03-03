from rest_framework import viewsets

from apidata.serializers.provinsi_serializer import ProvinsiSerializer
from master.models import Provinsi


class ProvinsiViewSet(viewsets.ModelViewSet):
    queryset = Provinsi.objects.all()
    serializer_class = ProvinsiSerializer
    http_method_names = ["get", "head"]
