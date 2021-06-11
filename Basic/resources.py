from django.db.models import fields
from import_export import resources
from import_export.fields import Field
from .models import DataAVM, Pozo


class DataPozoResource(resources.ModelResource):
    ESTADO = Field(attribute='estado')
    SARTA = Field(attribute='nombre')

    class Meta:
        model = Pozo
        import_id_fields = ('SARTA',)
        fields = ('SARTA', 'ESTADO',)
