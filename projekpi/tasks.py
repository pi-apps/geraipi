import time

from celery import shared_task
from master.models import Region, SubRegion, Country, Provinsi, Regency, Distric, Village


@shared_task(name="api_check_availability")
def check_availability():
    time.sleep(20)
    print("hello")
    
@shared_task(name="import_region")
def import_region(region={}):
    region_model = Region.objects.filter(id=region.get("id"),name=region.get("name", "-"), wiki_id=region.get("wikiDataId", "-")).first()
    if region_model:
        print("Is Exists")
    else:
        region_model = Region.objects.create(id=region.get("id"),name=region.get("name", "-"), wiki_id=region.get("wikiDataId", "-"))
        print("Saved Done ")

@shared_task(name="import_subregion")
def import_subregion(subregion={}):
    subregion_model = SubRegion.objects.filter(name=subregion.get("name", "-"), region_id_id=subregion.get('region_id'), wiki_id=subregion.get("wikiDataId", "-")).first()
    if subregion_model:
        print("is Exists")
    else:
        region = Region.objects.get(id=subregion.get('region_id'))
        subregion_model = SubRegion.objects.create(id=subregion.get("id") ,name=subregion.get("name", "-"), region_id=region, wiki_id=subregion.get("wikiDataId", "-"))
        print("Success saved")
        
@shared_task(name="import_country")
def import_country(countries={}):
    region = countries.get('region_id', None)
    subregion = countries.get('subregion_id', None)
    name = countries.get('name')
    countries_model = Country.objects.filter(
        region_id_id = region,
        subregion_id_id = subregion,
        name = name
    ).first()
    if countries_model:
        print("is exist countri")
    else:
        countries_model = Country.objects.create(
            id = countries.get('id'),
            region_id_id = region,
            subregion_id_id = subregion,
            name = name,
            iso3 = countries.get('iso3'),
            iso2 = countries.get('iso2'),
            numeric_code = countries.get('numeric_code'),
            phone_code = countries.get('phone_code'),
            capital = countries.get('capital'),
            currency = countries.get('currency'),
            currency_name = countries.get('currency_name'),
            currency_symbol = countries.get('currency_symbol'),
            tld = countries.get('tld'),
            native = countries.get('native'),
            nationality = countries.get('nationality'),
            timezones = countries.get('timezones', None)
        )
        print("saved country")
