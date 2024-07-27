from django.core import serializers
from django.core.management.base import BaseCommand

from produk import models


class Command(BaseCommand):
    help = "export warna produk"

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.WarnaProduk.objects.all())
        out = open("data/warna_produk.json", "w")
        out.write(data)
        out.close()
