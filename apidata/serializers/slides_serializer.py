from rest_framework import serializers

from frontend.models import Banner


class BannerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Banner
        fields = ["url", "name", "image"]
