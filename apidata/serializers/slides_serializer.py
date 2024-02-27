from frontend.models import Banner
from rest_framework import serializers


class BannerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Banner
        fields = ['url', 'name', 'image']

