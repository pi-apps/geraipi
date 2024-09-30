from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from master.models.country import Country
from master.models.region import Region
from master.models.subregion import SubRegion


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


# Register your models here.
