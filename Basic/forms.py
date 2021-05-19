from django import forms


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
        choices=CHOICES, required=True, label="Tipo calculo", widget= forms.RadioSelect, initial='apiMezcla')
    variableACalcular = forms.DecimalField(
        decimal_places=2, required=True, label="Diluyente a inyectar BPD")

    

