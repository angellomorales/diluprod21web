from django.db.models import fields
from import_export import resources
from import_export.fields import Field
from .models import DataAVM, Pozo


class DataPozoResource(resources.ModelResource):
    ESTADO = Field(attribute='estado', saves_null_values=False)
    SARTA = Field(attribute='nombre', saves_null_values=False)

    def skip_row(self, instance, original):
        skip=getattr(instance, 'pk') is ''
        return skip

    class Meta:
        model = Pozo
        import_id_fields = ('SARTA',)
        fields = ('SARTA', 'ESTADO',)
