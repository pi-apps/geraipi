from django.core import serializers
from django.core.management.base import BaseCommand

from frontend import models

# from produk import models


class Command(BaseCommand):
    help = "export master banner"

    # # def add_arguments(self, parser):
    # #     parser.add_argument("poll_ids", nargs="+", type=int)

    # def get_memory(self):
    #     with open('/proc/meminfo', 'r') as mem:
    #         free_memory = 0
    #         for i in mem:
    #             sline = i.split()
    #             if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
    #                 free_memory += int(sline[1])
    #     return free_memory  # KiB

    # def memory_limit_half(self):
    #     """Limit max memory usage to half."""
    #     soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    #     # Convert KiB to bytes, and divide in two to half
    #     resource.setrlimit(resource.RLIMIT_AS, (int(self.get_memory() * 1024 / 2), hard))

    def handle(self, *args, **options):
        data = serializers.serialize("json", models.Banner.objects.all())
        out = open("data/banner.json", "w")
        out.write(data)
        out.close()
