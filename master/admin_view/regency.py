from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from master.models.provinsi import Provinsi
from master.models.regency import Regency


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

