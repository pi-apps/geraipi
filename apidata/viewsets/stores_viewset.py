from rest_framework import viewsets

from apidata.serializers.stores_serializer import (
    UserStoreAddressSerializer,
    UserStoreSerializer,
)
from store.models import UserStore, UserStoreAddress


class UserStoreViewset(viewsets.ModelViewSet):
    queryset = UserStore.objects.all()
    serializer_class = UserStoreSerializer
    http_method_names = ["get", "head", "option"]


class UserStoreAddressViewset(viewsets.ModelViewSet):
    queryset = UserStoreAddress.objects.all()
    serializer_class = UserStoreAddressSerializer
    http_method_names = ["get", "head", "option"]
