import csv
import json
import time

from celery import shared_task

from master.models.country import Country
from master.models.distric import Distric
from master.models.provinsi import Provinsi
from master.models.regency import Regency
from master.models.region import Region
from master.models.subregion import SubRegion
from master.models.village import Village


@shared_task(name="api_check_availability")
def check_availability():
    time.sleep(20)
    print("hello")


@shared_task(name="import_all")
def import_all_alamat(reset=False):
    if reset:
        Village.objects.all().delete()
        Distric.objects.all().delete()
        Regency.objects.all().delete()
        Provinsi.objects.all().delete()
        Country.objects.all().delete()
        SubRegion.objects.all().delete()
        Region.objects.all().delete()
    import_region()
    print("done import region")
    import_subregion()
    print("done import subregion")
    import_country()
    print("done import Country")
    import_provinsi()
    print("done import provinsi")
    import_regency()
    print("done import regency")
    import_district()
    print("done import district")
    import_village()
    print("done import village")


@shared_task(name="import_region")
def import_region():
    with open("data/regions.json", encoding="utf-8", errors="ignore") as read_file:
        data = json.load(read_file)
        for region in data:
            region_model = Region.objects.filter(
                id=region.get("id"),
                name=region.get("name", "-"),
                wiki_id=region.get("wikiDataId", "-"),
            ).first()
            if region_model:
                print("Is Exists")
            else:
                region_model = Region.objects.create(
                    id=region.get("id"),
                    name=region.get("name", "-"),
                    wiki_id=region.get("wikiDataId", "-"),
                )
                print("Saved Done ")


@shared_task(name="import_subregion")
def import_subregion():
    with open("data/subregions.json", encoding="utf-8", errors="ignore") as read_subregion:
        data_subregion = json.load(read_subregion)
        for subregion in data_subregion:
            subregion_model = SubRegion.objects.filter(
                name=subregion.get("name", "-"),
                region_id_id=subregion.get("region_id"),
                wiki_id=subregion.get("wikiDataId", "-"),
            ).first()
            if subregion_model:
                print("is Exists")
            else:
                region = Region.objects.get(id=subregion.get("region_id"))
                subregion_model = SubRegion.objects.create(
                    id=subregion.get("id"),
                    name=subregion.get("name", "-"),
                    region_id=region,
                    wiki_id=subregion.get("wikiDataId", "-"),
                )
                print("Success saved")


@shared_task(name="import_country")
def import_country():
    with open("data/countries.json", encoding="utf-8", errors="ignore") as read_countries:
        data_countries = json.load(read_countries)
        for countries in data_countries:
            region = countries.get("region_id", None)
            subregion = countries.get("subregion_id", None)
            name = countries.get("name")
            countries_model = Country.objects.filter(region_id_id=region, subregion_id_id=subregion, name=name).first()
            if countries_model:
                print("is exist countri")
            else:
                countries_model = Country.objects.create(
                    id=countries.get("id"),
                    region_id_id=region,
                    subregion_id_id=subregion,
                    name=name,
                    iso3=countries.get("iso3"),
                    iso2=countries.get("iso2"),
                    numeric_code=countries.get("numeric_code"),
                    phone_code=countries.get("phone_code"),
                    capital=countries.get("capital"),
                    currency=countries.get("currency"),
                    currency_name=countries.get("currency_name"),
                    currency_symbol=countries.get("currency_symbol"),
                    tld=countries.get("tld"),
                    native=countries.get("native"),
                    nationality=countries.get("nationality"),
                    timezones=countries.get("timezones", None),
                )
                print("saved country")


@shared_task(name="import_provinsi")
def import_provinsi():
    with open("data/provinces.csv") as read_provice:
        spamreader = csv.reader(read_provice)
        for row in spamreader:
            code = row[0]
            name = row[1]
            province_model = Provinsi.objects.filter(id=code, code=code, nama=name).first()
            if province_model:
                print("Province exists")
            else:
                province_model = Provinsi.objects.create(id=code, code=code, nama=name)
                print("Province saved")


@shared_task(name="import_regency")
def import_regency():
    with open("data/regencies.json", encoding="utf-8", errors="ignore") as read_regency:
        spamreader = json.load(read_regency)
        for row in spamreader:
            code = row.get("code")
            province_code = row.get("province")
            name = row.get("name")
            province_model = Regency.objects.filter(
                id=code, code=code, province_code_id=province_code, name=name
            ).first()
            if province_model:
                print("regency exist")
            else:
                province_model = Regency.objects.create(id=code, code=code, province_code_id=province_code, name=name)
                print("regency saved")


@shared_task(name="import_district")
def import_district():
    with open("data/district.json", encoding="utf-8", errors="ignore") as read_district:
        spamreader = json.load(read_district)
        for row in spamreader:
            code = row.get("code")
            regency_code = row.get("regency")
            name = row.get("name")
            province_model = Distric.objects.filter(id=code, code=code, regency_code_id=regency_code, name=name).first()
            if province_model:
                print("District exist")
            else:
                province_model = Distric.objects.create(id=code, code=code, regency_code_id=regency_code, name=name)
                print("District saved")


@shared_task(name="import_village")
def import_village():
    with open("data/village.json", encoding="utf-8", errors="ignore") as read_village:
        spamreader = json.load(read_village)
        for row in spamreader:
            code = row.get("code")
            district_code = row.get("distric")
            name = row.get("name")
            village_model = Village.objects.filter(code=code, district_code_id=district_code, name=name).first()
            if village_model:
                print("Village Exists")
            else:
                Village.objects.create(code=code, district_code_id=district_code, name=name)
                print("Village saved")
