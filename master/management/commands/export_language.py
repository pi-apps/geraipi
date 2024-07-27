from django.core import serializers
from django.core.management.base import BaseCommand

from profiles import models


class Command(BaseCommand):
    help = "export Language"

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.LangSupport.objects.all())
        out = open("data/language.json", "w")
        out.write(data)
        out.close()
