from import_export import resources
from import_export.admin import ImportExportModelAdmin

from master.models.provinsi import Provinsi


class ProvinsiResource(resources.ModelResource):
    class Meta:
        model = Provinsi
        import_id_fields = ["id"]


class ProvinsiAdmin(ImportExportModelAdmin):
    resource_classes = [ProvinsiResource]

