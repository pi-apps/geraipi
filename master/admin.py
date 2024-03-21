from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from solo.admin import SingletonModelAdmin

from .models import (
    ConfigurationWebsite,
    Country,
    Distric,
    HistoriTampung,
    Provinsi,
    Regency,
    Region,
    SettingWebsite,
    SubRegion,
    Village,
)

admin.site.register(ConfigurationWebsite, SingletonModelAdmin)
admin.site.register(HistoriTampung)


class ProvinsiResource(resources.ModelResource):
    class Meta:
        model = Provinsi
        import_id_fields = ["id"]


class ProvinsiAdmin(ImportExportModelAdmin):
    resource_classes = [ProvinsiResource]


admin.site.register(Provinsi, ProvinsiAdmin)


class RegencyResource(resources.ModelResource):
    province_code = fields.Field(
        column_name="province_code",
        attribute="province_code",
        widget=ForeignKeyWidget(Provinsi, field="code"),
    )

    class Meta:
        model = Regency
        import_id_fields = ["id"]


class RegencyAdmin(ImportExportModelAdmin):
    resource_classes = [RegencyResource]


admin.site.register(Regency, RegencyAdmin)


class DistricResource(resources.ModelResource):
    regency_code = fields.Field(
        column_name="regency_code",
        attribute="regency_code",
        widget=ForeignKeyWidget(Regency, field="code"),
    )

    class Meta:
        model = Distric
        import_id_fields = ["id"]


class DistricAdmin(ImportExportModelAdmin):
    resource_classes = [DistricResource]


admin.site.register(Distric, DistricAdmin)


class VillageResource(resources.ModelResource):
    district_code = fields.Field(
        column_name="district_code",
        attribute="district_code",
        widget=ForeignKeyWidget(Distric, field="code"),
    )

    class Meta:
        model = Village
        import_id_fields = ["id"]


class VillageAdmin(ImportExportModelAdmin):
    resource_classes = [VillageResource]


admin.site.register(Village, VillageAdmin)

admin.site.register(SettingWebsite)


class RegionResource(resources.ModelResource):
    wiki_id = fields.Field(column_name="wiki_id", attribute="wiki_id")

    class Meta:
        model = Region
        import_id_fields = ["id"]


class RegionAdmin(ImportExportModelAdmin):
    resource_classes = [RegionResource]


admin.site.register(Region, RegionAdmin)


class SubRegionResource(resources.ModelResource):
    region_id = fields.Field(
        column_name="region_id",
        attribute="region_id",
        widget=ForeignKeyWidget(Region, field="id"),
    )

    class Meta:
        model = SubRegion
        import_id_fields = ["id"]


class SubRegionAdmin(ImportExportModelAdmin):
    resource_classes = [SubRegionResource]


admin.site.register(SubRegion, SubRegionAdmin)


class CountryResource(resources.ModelResource):
    region_id = fields.Field(
        column_name="region_id",
        attribute="region_id",
        widget=ForeignKeyWidget(Region, field="id"),
    )

    subregion_id = fields.Field(
        column_name="subregion_id",
        attribute="subregion_id",
        widget=ForeignKeyWidget(SubRegion, field="id"),
    )

    class Meta:
        model = Country
        import_id_fields = ["id"]


class CountryAdmin(ImportExportModelAdmin):
    resource_classes = [CountryResource]


admin.site.register(Country, CountryAdmin)

# Register your models here.
