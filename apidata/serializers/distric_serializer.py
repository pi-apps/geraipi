from rest_framework import serializers

from master.models.distric import Distric


class DistricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distric
        fields = ["url", "id", "code", "regency_code", "name"]
