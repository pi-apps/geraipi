from django.core import serializers
from django.core.management.base import BaseCommand

from profiles import models


class Command(BaseCommand):
    help = "export Language"

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.UserProfile.objects.all())
        with open("data/profile.json", "w", encoding="utf-8") as f:
            f.write(data)
            f.close()
