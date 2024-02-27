from django.contrib import admin
from .models import Provinsi, Regency, Distric, Village, SettingWebsite, HistoriTampung, ConfigurationWebsite
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from solo.admin import SingletonModelAdmin

admin.site.register(ConfigurationWebsite, SingletonModelAdmin)
admin.site.register(HistoriTampung)

class ProvinsiResource(resources.ModelResource):
    class Meta:
        model = Provinsi
        import_id_fields = ['id']

class ProvinsiAdmin(ImportExportModelAdmin):
    resource_classes = [ProvinsiResource]

admin.site.register(Provinsi, ProvinsiAdmin)

class RegencyResource(resources.ModelResource):
    province_code = fields.Field(
        column_name='province_code',
        attribute='province_code',
        widget=ForeignKeyWidget(Provinsi, field='code')
    )
    class Meta:
        model = Regency
        import_id_fields = ['id']

class RegencyAdmin(ImportExportModelAdmin):
    resource_classes = [RegencyResource]

admin.site.register(Regency, RegencyAdmin)

class DistricResource(resources.ModelResource):
    regency_code = fields.Field(
        column_name='regency_code',
        attribute='regency_code',
        widget=ForeignKeyWidget(Regency, field='code')
    )
    class Meta:
        model = Distric
        import_id_fields = ['id']

class DistricAdmin(ImportExportModelAdmin):
    resource_classes = [DistricResource]

admin.site.register(Distric, DistricAdmin)

class VillageResource(resources.ModelResource):
    district_code = fields.Field(
        column_name='district_code',
        attribute='district_code',
        widget=ForeignKeyWidget(Distric, field='code')
    )
    class Meta:
        model = Village
        import_id_fields = ['id']

class VillageAdmin(ImportExportModelAdmin):
    resource_classes = [VillageResource]

admin.site.register(Village, VillageAdmin)

admin.site.register(SettingWebsite)

# Register your models here.
