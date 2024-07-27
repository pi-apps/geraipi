from django.core import serializers
from django.core.management.base import BaseCommand

from store import models


class Command(BaseCommand):
    help = "export address store"

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.UserStoreAddress.objects.all())
        with open("data/store_address.json", "w") as f:
            f.write(data)
            f.close()
