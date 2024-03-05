from rest_framework import serializers

from master.models import Provinsi


class ProvinsiSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Provinsi
        fields = ["url", "id", "code", "nama"]
