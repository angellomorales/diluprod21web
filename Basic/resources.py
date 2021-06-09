from import_export import resources
from .models import DataAVM


class DataAVMResource(resources.ModelResource):
    class Meta:
        model = DataAVM
