from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.results import RowResult
from .models import Campo, DataAVM, DataStork, Pozo, PozoInyector
from decimal import Decimal


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
            # print(self.field, value)
            return self.get_queryset(value, row, *args, **kwargs).get(**{self.field: value}) if self.get_queryset(value, row, *args, **kwargs).exists() else None
        # else:
        #     raise ValueError(self.field + " required")

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
    API = Field(attribute='apiMezcla',
                column_name='API MEZCLA  @ 60 °F')
    COMENTARIOS = Field(attribute='comentarios', column_name='COMENTARIOS')

    def before_import_row(self, row, **kwargs):
        try:
            val = row[" % S&W (MULTIFASICO)"]
            if row[" % S&W"]:
                row[" % S&W"] = row[" % S&W"]*100
        except:
            raise ValueError(
                f"el archivo no contiene datos relacionados al modelo {self.Meta.model} que se esta cargando")

    def skip_row(self, instance, original):
        if not (getattr(original, 'dataAVM_id') == None):
            diff_orig = getattr(original, 'dataAVM').bsw / \
                100 - getattr(original, 'bsw')
            diff_actual = getattr(instance, 'dataAVM').bsw / \
                100 - Decimal(getattr(instance, 'bsw'))
            if diff_orig < diff_actual:
                return True
        skip = getattr(instance, 'dataAVM_id') == None
        return skip

    class Meta:
        model = DataStork
        skip_unchanged = True
        import_id_fields = ('POZO',)
        # exclude = ('id')
        fields = ('POZO', ' % S&W', 'FLUIDO TOTAL (BFPD)', ' % S&W (MULTIFASICO)', 'API MEZCLA  @ 60 °F',
                  'NAFTA INYECTADA (BPD) (MULTIFASICO)', 'COMENTARIOS')


class DataPozoInyectorResource(resources.ModelResource):
    POZO_INYECTOR = Field(attribute='pozoInyector', column_name='Pozo Inyector', widget=ForeignKeyWidget(
        Pozo, 'nombre'), saves_null_values=False)
    CAUDAL_INYECCION = Field(attribute='caudalInyeccion',
                             column_name='Objetivo de inyección (BWPD)', saves_null_values=False)
    FECHA_INICIO = Field(attribute='fechaInicio', column_name='Inicio de inyección',
                         saves_null_values=False)
    PROCESO = Field(attribute='proceso',
                    column_name='PROCESO', saves_null_values=False)
    # POZOS_ASOCIADOS = Field(attribute='pozosAsociados', column_name='Pozo productor asociado - Primera línea ', widget=ManyToManyWidget(
    #     Pozo, field='nombre'), saves_null_values=False) #asi se construye un manytomanywidget

    def after_import_row(self, row, row_result, **kwargs):
        if not(row_result.import_type == RowResult.IMPORT_TYPE_ERROR):
            instance = PozoInyector.objects.get(
                pozoInyector=row.get('Pozo Inyector'))
            instanceAsociado = Pozo.objects.filter(
                nombre=row.get('Pozo productor asociado - Primera línea '))
            if instanceAsociado.exists():
                instance.pozosAsociados.add(instanceAsociado.get())
            else:
                raise ValueError("Errores en la fila {}: {}".format(kwargs['row_number']+1, "el pozo asociado no existe"))

    # # https://github.com/django-import-export/django-import-export/issues/763
    #     # overriding import_row to ignore errors and skip rows that fail to import
    #     # without failing the entire import
    #     #para saltarse la fila ante un error y seguir importando
    # def import_row(self, row, instance_loader, **kwargs):
    #     import_result = super().import_row(row, instance_loader, **kwargs)
    #     if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
    #         if (not(Pozo.objects.filter(nombre=row.get('Pozo Inyector')).exists())
    #                 or (not(Pozo.objects.filter(nombre=row.get('Pozo productor asociado - Primera línea ')).exists()))):
    #             print("Errors in row {}: {}".format(kwargs['row_number'], [
    #                   err.error for err in import_result.errors]))  # show error
    #             import_result.errors = []  # saltar la fila pero seguir importando
    #             import_result.import_type = RowResult.IMPORT_TYPE_SKIP
    #     return import_result

    class Meta:
        model = PozoInyector
        skip_unchanged = True
        import_id_fields = ('POZO_INYECTOR',)
        exclude = ('id')
        fields = ('Pozo Inyector', 'Objetivo de inyección (BWPD)',
                  'Inicio de inyección', 'Pozo productor asociado - Primera línea ', 'PROCESO')


class DataLaboratorioResource(resources.ModelResource):
    def import_data(self, *args, **kwargs):
        raise ValueError(
            f"Funcionalidad data Laboratorio deshabilitada temporalmente")
