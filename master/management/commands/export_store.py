from django.core import serializers
from django.core.management.base import BaseCommand

from store import models


class Command(BaseCommand):
    help = "export Store"

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.UserStore.objects.all())
        with open("data/store.json", "w", encoding="utf-8") as f:
            f.write(data)
            f.close()
