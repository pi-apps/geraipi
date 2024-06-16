from django.core.management.base import BaseCommand, CommandError
from master.models import Region, SubRegion, Country, Provinsi, Regency, Distric, Village
import json
import csv
import sys


class Command(BaseCommand):
    help = "Sync Region"

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
        from projekpi.tasks import import_region, import_subregion, import_country
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
                
        # self.memory_limit_half()
        # try:
            # Region.objects.all().delete()
            # with open("data/regions.json", encoding='utf-8', errors='ignore') as read_file:
            #     data = json.load(read_file)
            #     for region in data:
            #         import_region.delay(region)
            # SubRegion.objects.all().delete()
            # with open("data/subregions.json", encoding='utf-8', errors='ignore') as read_subregion:
            #     data_subregion = json.load(read_subregion)
            #     for subregion in data_subregion:
            #         subregion_model = SubRegion.objects.filter(name=subregion.get("name", "-"), region_id_id=subregion.get('region_id'), wiki_id=subregion.get("wikiDataId", "-")).first()
            #         if subregion_model:
            #             self.stdout.write(
            #                 self.style.SUCCESS('subregion exists')
            #             )
            #         else:
            #             region = Region.objects.get(id=subregion.get('region_id'))
            #             subregion_model = SubRegion.objects.create(id=subregion.get("id") ,name=subregion.get("name", "-"), region_id=region, wiki_id=subregion.get("wikiDataId", "-"))
            #             self.stdout.write(
            #                 self.style.SUCCESS('subregion Save Done')
            #             )
            # Country.objects.all().delete()
            # with open('data/countries.json', encoding='utf-8', errors='ignore') as read_countries:
            #     data_countries = json.load(read_countries)
            #     for countries in data_countries:
            #         region = countries.get('region_id', None)
            #         subregion = countries.get('subregion_id', None)
            #         name = countries.get('name')
            #         countries_model = Country.objects.filter(
            #             region_id_id = region,
            #             subregion_id_id = subregion,
            #             name = name
            #         ).first()
            #         if countries_model:
            #             self.stdout.write(
            #                 self.style.SUCCESS('Countries exists')
            #             )
            #         else:
            #             countries_model = Country.objects.create(
            #                 id = countries.get('id'),
            #                 region_id_id = region,
            #                 subregion_id_id = subregion,
            #                 name = name,
            #                 iso3 = countries.get('iso3'),
            #                 iso2 = countries.get('iso2'),
            #                 numeric_code = countries.get('numeric_code'),
            #                 phone_code = countries.get('phone_code'),
            #                 capital = countries.get('capital'),
            #                 currency = countries.get('currency'),
            #                 currency_name = countries.get('currency_name'),
            #                 currency_symbol = countries.get('currency_symbol'),
            #                 tld = countries.get('tld'),
            #                 native = countries.get('native'),
            #                 nationality = countries.get('nationality'),
            #                 timezones = countries.get('timezones', None)
            #             )
            #             self.stdout.write(
            #                 self.style.SUCCESS('subregion Success saved')
            #             )
            # Provinsi.objects.all().delete()
            # with open("data/provinces.csv") as read_provice:
            #     spamreader = csv.reader(read_provice)
            #     for row in spamreader:
            #         code = row[0]
            #         name = row[1]
            #         province_model = Provinsi.objects.filter(id=code, code=code, nama=name).first()
            #         if province_model:
            #             self.stdout.write(
            #                 self.style.SUCCESS('Provinsi exists')
            #             )
            #         else:
            #             province_model = Provinsi.objects.create(id=code, code=code, nama=name)
            #             self.stdout.write(
            #                 self.style.SUCCESS('Provinsi Success saved')
            #             )
            # Regency.objects.all().delete()
            # with open('data/regencies.json', encoding='utf-8', errors='ignore') as read_regency:
            #     spamreader = json.load(read_regency)
            #     for row in spamreader:
            #         code = row.get('code')
            #         province_code = row.get("province")
            #         name = row.get("name")
            #         province_model = Regency.objects.filter(id=code, code=code, province_code_id=province_code, name=name).first()
            #         if province_model:
            #             self.stdout.write(
            #                 self.style.SUCCESS('Regency exists')
            #             )
            #         else:
            #             province_model = Regency.objects.create(id=code, code=code, province_code_id=province_code, name=name)
            #             self.stdout.write(
            #                 self.style.SUCCESS('Regency Success saved')
            #             )
            # Distric.objects.all().delete()
            # with open('data/district.json', encoding='utf-8', errors='ignore') as read_district:
            #     spamreader = json.load(read_district)
            #     for row in spamreader:
            #         print(row)
            #         code = row.get('code')
            #         regency_code = row.get('regency')
            #         name = row.get("name")
            #         province_model = Distric.objects.filter(id=code, code=code, regency_code_id=regency_code, name=name).first()
            #         if province_model:
            #             self.stdout.write(
            #                 self.style.SUCCESS('Distric exists')
            #             )
            #         else:
            #             province_model = Distric.objects.create(id=code, code=code, regency_code_id=regency_code, name=name)
            #             self.stdout.write(
            #                 self.style.SUCCESS('Distric Success saved')
            #             )
            # Village.objects.all().delete()
            # with open('data/village.json', encoding='utf-8', errors='ignore') as read_village:
            #     spamreader = json.load(read_village)
            #     for row in spamreader:
            #         code = row.get('code')
            #         district_code = row.get('distric')
            #         name = row.get('name')
            #         village_model = Village.objects.filter(code=code, district_code_id=district_code, name=name).first()
            #         if village_model:
            #             self.stdout.write(
            #                 self.style.SUCCESS('Village exists')
            #             )
            #         else:
            #             province_model = Village.objects.create(code=code, district_code_id=district_code, name=name)
            #             self.stdout.write(
            #                 self.style.SUCCESS('Village Success saved')
            #             )
        # except MemoryError:
        #     sys.stderr.write('\n\nERROR: Memory Exception\n')
        #     sys.exit(1)

