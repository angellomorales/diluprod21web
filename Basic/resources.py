from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import Campo, DataAVM, DataStork, Pozo


# class ForeignKeyWidgetWithCreation(ForeignKeyWidget):

#     def __init__(self, model, field="pk", create=False, **kwargs):
#         self.model = model
#         self.field = field
#         self.create = create
#         # super(ForeignKeyWidgetWithCreation, self).__init__(
#         #     model, field=field, **kwargs)

#     def clean(self, value, **kwargs):
#         if not value:
#             return None

#         if self.create:
#             instance, new = self.model.objects.get_or_create(
#                 **{self.field: value})

#         val = super(ForeignKeyWidgetWithCreation, self).clean(value, **kwargs)

#         return self.model.objects.get(**{self.field: val}) if val else None
#         # es lo mismo que lo de arriba
#         # if val:
#         #     myreturnobj=self.model.objects.get(**{self.field: val})
#         #     # return myreturnobj
#         # else:
#         #     return None


# class StoreWidget(ForeignKeyWidget):
#     def clean(self, value, **kwargs):
#         return self.model.objects.get_or_create(nombre=value)


class ForeignKeyWidgetMultipleFields(ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if value:
            print(self.field, value)
            return self.get_queryset(value, row, *args, **kwargs).get(**{self.field: value}) if self.get_queryset(value, row, *args, **kwargs).exists() else None
        else:
            raise ValueError(self.field + " required")

    def get_queryset(self, value, row):
        return self.model.objects.filter(pozo=row["POZO"], fecha=row["FECHA DE INICIO DE LA PRUEBA"])


class DataPozoResource(resources.ModelResource):
    ESTADO = Field(attribute='estado', saves_null_values=False)
    SARTA = Field(attribute='nombre', saves_null_values=False)

    def skip_row(self, instance, original):
        skip = getattr(instance, 'nombre') == ''
        return skip

    class Meta:
        model = Pozo
        import_id_fields = ('SARTA',)
        fields = ('SARTA', 'ESTADO',)


class DataAVMResource(resources.ModelResource):
    CAMPO = Field(attribute='campo', column_name='CAMPO', widget=ForeignKeyWidget(
        Campo, 'nombre'), saves_null_values=False)

    SARTA = Field(attribute='pozo', column_name='SARTA', widget=ForeignKeyWidget(
        Pozo, 'nombre'), saves_null_values=False)
    # no funcionaron bien
    # SARTA = Field(attribute='pozo', column_name='SARTA', widget=StoreWidget(
    #     Pozo, 'nombre'), saves_null_values=False)
    # SARTA = Field(attribute='pozo', column_name='SARTA', saves_null_values=False, widget=ForeignKeyWidgetWithCreation(
    #     model=Pozo,
    #     field='nombre',
    #     create=True))

    FECHA = Field(attribute='fecha', column_name='FECHA',
                  saves_null_values=False)
    BSW = Field(attribute='bsw', column_name='BSW')
    API = Field(attribute='api', column_name='API')
    TASA_DE_LIQUIDO = Field(attribute='tasaLiquido',
                            column_name='TASA DE LIQUIDO')
    TASA_DE_GAS = Field(attribute='tasaGas', column_name='TASA DE GAS')
    TASA_DE_AGUA = Field(attribute='tasaAgua', column_name='TASA DE AGUA')
    TASA_DE_ACEITE = Field(attribute='tasaAceite',
                           column_name='TASA DE ACEITE')
    GOR = Field(attribute='gor', column_name='GOR')
    THP = Field(attribute='thp', column_name='THP')
    VELOCIDAD_BOMBA = Field(attribute='velocidadBomba',
                            column_name='VELOCIDAD BOMBA')
    CORRIENTE_VSD = Field(attribute='corrienteVSD',
                          column_name='CORRIENTE VSD')
    PIP = Field(attribute='pip', column_name='PIP')
    VOLTAJE_OUT_VSD = Field(attribute='voltajeOutVSD',
                            column_name='VOLTAJE OUT VSD')
    TEMP__CABEZA = Field(attribute='tempCabeza', column_name='TEMP_ CABEZA')
    PRUEBA_VALIDA = Field(attribute='pruebaValida',
                          column_name='PRUEBA VALIDA', saves_null_values=False)
    COMENTARIOS = Field(attribute='comentarios', column_name='COMENTARIOS')
    SALINIDAD = Field(attribute='salinidad', column_name='SALINIDAD')

    def before_import_row(self, row, **kwargs):
        if not(row.get('SARTA') == None):
            instancePozo, new = Pozo.objects.get_or_create(
                nombre=row.get('SARTA'),
                # https://stackoverflow.com/questions/19362085/get-or-create-throws-integrity-error
                defaults={'estado': row.get('ESTADO')}
            )
            instanceCampo, new2 = Campo.objects.get_or_create(
                nombre=row.get('CAMPO')
            )
            if new:
                instanceCampo.pozos.add(instancePozo)
        else:
            raise ValueError(
                f"el archivo no contiene datos relacionados al modelo {self.Meta.model} que se esta cargando")

    class Meta:
        model = DataAVM
        skip_unchanged = True
        import_id_fields = ('SARTA', 'FECHA')
        exclude = ('id')
        fields = ('SARTA', 'ESTADO', 'FECHA', 'BSW', 'API', 'TASA DE LIQUIDO', 'TASA DE GAS', 'TASA DE AGUA', 'TASA DE ACEITE', 'GOR',
                  'THP', 'VELOCIDAD BOMBA', 'CORRIENTE VSD', 'PIP', 'VOLTAJE OUT VSD', 'TEMP_ CABEZA', 'PRUEBA VALIDA', 'COMENTARIOS', 'SALINIDAD')


class DataStorkResource(resources.ModelResource):
    POZO = Field(attribute='dataAVM', column_name='POZO', widget=ForeignKeyWidgetMultipleFields(
        DataAVM, 'pozo'), saves_null_values=False)

    SW_MEZCLA = Field(attribute='swMezcla', column_name=' % S&W')
    DILUYENTE = Field(attribute='diluyenteInyectado',
                      column_name='NAFTA INYECTADA (BPD) (MULTIFASICO)')
    FLUIDO_TOTAL = Field(attribute='fluidoTotal',
                         column_name='FLUIDO TOTAL (BFPD)')
    BSW = Field(attribute='bsw',
                column_name=' % S&W (MULTIFASICO)')
    COMENTARIOS = Field(attribute='comentarios', column_name='COMENTARIOS')

    def skip_row(self, instance, original):
        skip = getattr(instance, 'dataAVM_id') == None
        return skip

    class Meta:
        model = DataStork
        skip_unchanged = True
        import_id_fields = ('POZO',)
        # exclude = ('id')
        fields = ('POZO', ' % S&W', 'FLUIDO TOTAL (BFPD)', ' % S&W (MULTIFASICO)',
                  'NAFTA INYECTADA (BPD) (MULTIFASICO)', 'COMENTARIOS')


class DataPozoInyectorResource(resources.ModelResource):
    def import_data(self, *args, **kwargs):
        raise ValueError(
            f"Funcionalidad Pozo Inyector deshabilitada temporalmente")


class DataLaboratorioResource(resources.ModelResource):
    def import_data(self, *args, **kwargs):
        raise ValueError(
            f"Funcionalidad data Laboratorio deshabilitada temporalmente")
