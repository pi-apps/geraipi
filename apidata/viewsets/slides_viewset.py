from rest_framework import viewsets

from apidata.serializers.slides_serializer import BannerSerializer
from frontend.models import Banner


class SlidesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    pagination_class = None
    http_method_names = ["get", "head"]
