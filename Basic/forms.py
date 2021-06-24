from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
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
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['aceite'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['swCabeza'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['apiCabeza'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['apiDiluyente'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['variableACalcular'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})


class LaboratorioForm(forms.Form):
    swMezcla = forms.DecimalField(
        decimal_places=2, required=True, label="% S&W Mezcla")
    apiMezcla = forms.DecimalField(
        decimal_places=2, required=True, label="API Mezcla @60ºF")

    def __init__(self, *args, **kwargs):
        super(LaboratorioForm, self).__init__(*args, **kwargs)
        self.fields['swMezcla'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['apiMezcla'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})


class DataHistoricaForm(ModelForm):
    class Meta:
        model = DataAVM
        fields = ['pozo']

    def __init__(self, *args, **kwargs):
        super(DataHistoricaForm, self).__init__(*args, **kwargs)
        self.fields['pozo'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
