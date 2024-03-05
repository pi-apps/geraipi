from rest_framework import serializers

from master.models import Regency


class RegencySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Regency
        fields = ["url", "id", "code", "province_code", "name"]
