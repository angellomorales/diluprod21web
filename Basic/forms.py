from django import forms


class NewCalculosForm(forms.Form):
    CHOICES = [('apiMezcla', 'Api de Mezcla'),
               ('diluyenteRequerido', 'Diluyente Requerido')]
    aceitePruebaAnterior = forms.DecimalField(
        decimal_places=2, required=True, label="Aceite Prueba Anterior BPD")
    fraccionSYWCabeza = forms.DecimalField(
        decimal_places=2, required=True, label="Fracción S&W Cabeza")
    APICabeza = forms.DecimalField(
        decimal_places=2, required=True, label="API Cabeza @60ºF")
    APIDiluyente = forms.DecimalField(
        decimal_places=2, required=True, label="API Diluyente @60ºF")
    TipoCalculo = forms.ChoiceField(
        choices=CHOICES, required=True, label="Tipo calculo", widget= forms.RadioSelect)
    APISeco = forms.DecimalField(
        decimal_places=2, required=True, label="API Seco @60ºF")

