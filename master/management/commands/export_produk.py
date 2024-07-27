from django.core import serializers
from django.core.management.base import BaseCommand

from produk import models


class Command(BaseCommand):
    help = "export produk"

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.Produk.objects.all())
        with open("data/produk.json", "w", encoding="utf-8") as f:
            f.write(data)
            f.close()

        data = serializers.serialize("json", models.DeskripsiProduk.objects.all())
        with open("data/produk_deskripsi.json", "w", encoding="utf-8") as f:
            f.write(data)
            f.close()

        data = serializers.serialize("json", models.GambarProduk.objects.all())
        with open("data/produk_gambar.json", "w", encoding="utf-8") as f:
            f.write(data)
            f.close()
