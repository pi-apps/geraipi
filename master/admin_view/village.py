from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from master.models.distric import Distric
from master.models.village import Village


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