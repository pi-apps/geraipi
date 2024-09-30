from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from master.models.region import Region
from master.models.subregion import SubRegion


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