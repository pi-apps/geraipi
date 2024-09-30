from django.contrib import admin
from solo.admin import SingletonModelAdmin

from master.admin_view.country import CountryAdmin
from master.admin_view.distric import DistricAdmin
from master.admin_view.provinsi import ProvinsiAdmin
from master.admin_view.regency import RegencyAdmin
from master.admin_view.region import RegionAdmin
from master.admin_view.subregion import SubRegionAdmin
from master.admin_view.village import VillageAdmin
from master.models.configuration_website import ConfigurationWebsite
from master.models.country import Country
from master.models.distric import Distric
from master.models.history_tampung import HistoriTampung
from master.models.provinsi import Provinsi
from master.models.regency import Regency
from master.models.region import Region
from master.models.setting_website import SettingWebsite
from master.models.subregion import SubRegion
from master.models.village import Village

admin.site.register(ConfigurationWebsite, SingletonModelAdmin)
admin.site.register(HistoriTampung)
admin.site.register(Provinsi, ProvinsiAdmin)
admin.site.register(Regency, RegencyAdmin)
admin.site.register(Distric, DistricAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(SettingWebsite)
admin.site.register(Region, RegionAdmin)
admin.site.register(SubRegion, SubRegionAdmin)
admin.site.register(Country, CountryAdmin)
