from rest_framework import serializers

from master.models import Provinsi


class ProvinsiSerializer(serializers.HyperlinkedModelSerializer):
    code = serializers.SerializerMethodField()
    nama = serializers.SerializerMethodField()

    class Meta:
        model = Provinsi
        fields = ["url", "code", "nama"]

    def get_code(self, obj):
        return obj.code

    def get_nama(self, obj):
        return obj.nama
