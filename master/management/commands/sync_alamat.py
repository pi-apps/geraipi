from django.core.management.base import BaseCommand, CommandError
from master.models import Region, SubRegion, Country, Provinsi, Regency, Distric, Village
import json
import csv
import sys


class Command(BaseCommand):
    help = "Sync Alamat"

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
        from projekpi.tasks import import_region, import_subregion, import_country, import_provinsi, import_regency, import_district, import_village
        Region.objects.all().delete()
        with open("data/regions.json", encoding='utf-8', errors='ignore') as read_file:
            data = json.load(read_file)
            for region in data:
                import_region.delay(region)
        SubRegion.objects.all().delete()
        with open("data/subregions.json", encoding='utf-8', errors='ignore') as read_subregion:
            data_subregion = json.load(read_subregion)
            for subregion in data_subregion:
                import_subregion.delay(subregion)
        
        Country.objects.all().delete()
        with open('data/countries.json', encoding='utf-8', errors='ignore') as read_countries:
            data_countries = json.load(read_countries)
            for countries in data_countries:
                import_country.delay(countries)
                
        Provinsi.objects.all().delete()
        with open("data/provinces.csv") as read_provice:
            spamreader = csv.reader(read_provice)
            for row in spamreader:
                import_provinsi.delay(row)
                
        Regency.objects.all().delete()
        with open('data/regencies.json', encoding='utf-8', errors='ignore') as read_regency:
            spamreader = json.load(read_regency)
            for row in spamreader:
                import_regency.delay(row)
                
        Distric.objects.all().delete()
        with open('data/district.json', encoding='utf-8', errors='ignore') as read_district:
            spamreader = json.load(read_district)
            for row in spamreader:
                import_district.delay(row)
                
        Village.objects.all().delete()
        with open('data/village.json', encoding='utf-8', errors='ignore') as read_village:
            spamreader = json.load(read_village)
            for row in spamreader:
                import_village.delay(row)
