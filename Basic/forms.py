from django import forms
from django.core import validators
from django.db.models import fields
from django.forms.models import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import DataAVM


class CalculosForm(forms.Form):
    CHOICES = [('apiMezcla', 'Calcular Api de Mezcla'),
               ('diluyenteRequerido', 'Calcular Diluyente Requerido')]
    pozo = forms.CharField(required=False, label="Pozo")
    aceite = forms.DecimalField(
        decimal_places=2, required=True, label="Aceite Prueba Anterior BPD")
    swCabeza = forms.DecimalField(
        decimal_places=2, required=True, label="% S&W Cabeza")
    apiCabeza = forms.DecimalField(
        decimal_places=2, required=True, label="API Cabeza @60ºF")
    apiDiluyente = forms.DecimalField(
        decimal_places=2, required=True, label="API Diluyente @60ºF")
    tipoCalculo = forms.ChoiceField(
        choices=CHOICES, required=True, label="Tipo calculo", widget=forms.RadioSelect, initial='apiMezcla')
    variableACalcular = forms.DecimalField(
        decimal_places=2, required=True, label="Diluyente a inyectar BPD")

    def __init__(self, *args, **kwargs):
        super(CalculosForm, self).__init__(*args, **kwargs)
        self.fields['pozo'].widget.attrs.update(
            {'class': 'form-control','list':'Pozos'})
        self.fields['aceite'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['swCabeza'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['apiCabeza'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['apiDiluyente'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['variableACalcular'].widget.attrs.update(
            {'class': 'form-control'})


class LaboratorioForm(forms.Form):
    pozo = forms.CharField(required=True, label="Pozo")
    swMezcla = forms.DecimalField(
        decimal_places=2, required=True, label="% S&W Mezcla")
    apiMezcla = forms.DecimalField(
        decimal_places=2, required=True, label="API Mezcla @60ºF")

    def __init__(self, *args, **kwargs):
        super(LaboratorioForm, self).__init__(*args, **kwargs)
        self.fields['pozo'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2','list':'Pozos'})
        self.fields['swMezcla'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['apiMezcla'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})


# class DataHistoricaForm(ModelForm):#para usar el ModelForm asignando un select para seleccionar todos los pozos
#     class Meta:
#         model = DataAVM
#         fields = ['pozo']

#     def __init__(self, *args, **kwargs):
#         super(DataHistoricaForm, self).__init__(*args, **kwargs)
#         self.fields['pozo'].widget.attrs.update(
#             {'class': 'form-select w-auto'})


class DataHistoricaForm(forms.Form):
    pozo = forms.CharField(required=True, label="Pozo")

    def __init__(self, *args, **kwargs):
        super(DataHistoricaForm, self).__init__(*args, **kwargs)
        self.fields['pozo'].widget.attrs.update(
            {'class': 'form-control','list':'Pozos'})

class CargarDatosForm(forms.Form):
    CHOICES = [('Data AVM', 'Data AVM'), ('Data Stork', 'Data Stork'),
               ('Data Pozo Inyector', 'Data Pozo Inyector'), ('Data Laboratorio', 'Data Laboratorio')]
    tipo = forms.ChoiceField(choices=CHOICES, required=True,
                             label="Archivo", widget=forms.Select, initial='Data AVM')
    # archivo = forms.FileField()
    archivo = forms.FileField(required=False)

    # def validate_file_extension(value):
    #     if not value.name.endswith('.pdf'):
    #         raise ValidationError(u'Error message')

    def clean(self):
        data = self.cleaned_data['archivo']

        # check if the content type is what we expect
        content_type = data.content_type
        if content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or content_type == 'application/vnd.ms-excel':
            return data
        else:
            raise ValidationError(_('Invalid content type'), code='invalid')
