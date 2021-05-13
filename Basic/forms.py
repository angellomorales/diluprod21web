from django import forms


class NewCalculosForm(forms.Form):
    CHOICES = [('apiMezcla', 'Calcular Api de Mezcla'),
               ('diluyenteRequerido', 'Calcular Diluyente Requerido')]
    aceitePruebaAnterior = forms.DecimalField(
        decimal_places=2, required=True, label="Aceite Prueba Anterior BPD")
    fraccionSYWCabeza = forms.DecimalField(
        decimal_places=2, required=True, label="% S&W Cabeza")
    APICabeza = forms.DecimalField(
        decimal_places=2, required=True, label="API Cabeza @60ºF")
    APIDiluyente = forms.DecimalField(
        decimal_places=2, required=True, label="API Diluyente @60ºF")
    tipoCalculo = forms.ChoiceField(
        choices=CHOICES, required=True, label="Tipo calculo", widget= forms.RadioSelect)
    variableACalcular = forms.DecimalField(
        decimal_places=2, required=True, label="Variable a calcular")

