from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin

from master.models.region import Region


class RegionResource(resources.ModelResource):
    wiki_id = fields.Field(column_name="wiki_id", attribute="wiki_id")

    class Meta:
        model = Region
        import_id_fields = ["id"]


class RegionAdmin(ImportExportModelAdmin):
    resource_classes = [RegionResource]