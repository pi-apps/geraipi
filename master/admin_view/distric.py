from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from master.models.distric import Distric
from master.models.regency import Regency


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

