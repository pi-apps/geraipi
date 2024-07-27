from django.core import serializers
from django.core.management.base import BaseCommand

from produk import models


class Command(BaseCommand):
    help = "export tipe produk"

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.TipeProduk.objects.all())
        out = open("data/tipe_produk.json", "w")
        out.write(data)
        out.close()
