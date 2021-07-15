import json
from tablib import Dataset

from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import DataAVM, User
from .forms import CalculosForm, DataHistoricaForm, LaboratorioForm
from .calculos import Calculos
from .resources import DataAVMResource, DataPozoResource
from .representations import Representations
from .grafica import Grafica


def index(request):
    return render(request, "Basic/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Basic/login.html", {
                "message": "Usuario y/o Contraseña invalido."
            })
    else:
        return render(request, "Basic/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="index")
def calculos_view(request):
    if request.method == "POST":
        form = CalculosForm(request.POST)
        if form.is_valid():
            pozo = form.cleaned_data["pozo"]
            aceite = form.cleaned_data["aceite"]
            swCabeza = form.cleaned_data["swCabeza"]
            apiCabeza = form.cleaned_data["apiCabeza"]
            apiDiluyente = form.cleaned_data["apiDiluyente"]
            tipoCalculo = form.cleaned_data["tipoCalculo"]
            variableACalcular = form.cleaned_data["variableACalcular"]
            calculos = Calculos()
            if tipoCalculo == 'apiMezcla':
                calculos.calcularAPI(
                    apiCabeza, apiDiluyente, variableACalcular, aceite, swCabeza)
            else:
                calculos.calcularDiluyente(
                    apiCabeza, apiDiluyente, variableACalcular, aceite, swCabeza, True)
            representation = Representations()
            data = representation.representacionCalculos(calculos)
            return render(request, "Basic/calculos.html", {
                "form": form,
                "esCalculado": True,
                "data": data
            })
        else:
            # form.fields['category'].choices = CategoryChoices.choices#add a choices in category
            return render(request, "Basic/calculos.html", {
                "form": form
            })
    form = CalculosForm()
    return render(request, "Basic/calculos.html", {
        "form": form
    })


@login_required(login_url="index")
def graficarCalculos_view(request, graphId):
    if request.method == "POST":
        data = json.loads(request.body)
        calculos = Calculos()
        pozo = data.get("pozo")
        aceite = data["aceite"]
        apiCabeza = data["apiCabeza"]
        apiDiluyente = data.get("apiDiluyente")
        variableACalcular = data.get("apiMezclaHumedo")
        idContenedor = data.get("idContenedor")
        dataGraph = []  # list
        maxYValue = 1500

        for i in range(99):
            calculos.calcularDiluyente(
                apiCabeza, apiDiluyente, variableACalcular, aceite, i, False)

            # ------------------------------------------graph1---------------------------------------------
            if graphId == "relacionDiluyente":
                # configurar para cada grafica
                series1 = 's&w'
                series2 = 'relacionOil_Diluyente'
                title = 'Relación diluyente para API mezcla definido'
                titleXAxis = 'Porcentaje S&W'
                titleYAxis = 'Fracción volumétrica mezcla x % S&W cabeza'
                labelSeries1 = 'Fracción Volumétrica de Agua de Mezcla'
                labelSeries2 = 'Relación Diluyente/Mezcla'
                maxYValue = 1

                dataGraph.append(
                    {'x': str(i), series1: calculos.swMezcla, series2: calculos.relacionOil_Diluyente})  # dict

            # ------------------------------------------graph2---------------------------------------------
            if graphId == "diluyenteRequerido":
                # configurar para cada grafica
                series1 = 'diluyente'
                series2 = 'relacion1_3'
                title = 'Diluyente Requerido para API mezcla definido'
                titleXAxis = 'Porcentaje S&W'
                titleYAxis = 'BPD'
                labelSeries1 = 'Diluyente A Inyectar'
                labelSeries2 = 'Relacion 1-3'
                if(abs(calculos.diluyente-calculos.relacion1_3) < 20):
                    maxYValue = round(calculos.diluyente*2)

                dataGraph.append(
                    {'x': str(i), series1: calculos.diluyente, series2: calculos.relacion1_3})  # dict

            # ------------------------------------------graph3---------------------------------------------
            if graphId == "limiteRestriccion":
                # configurar para cada grafica
                series1 = 'apiMezclaSeco'
                series2 = 'limiteSuperior'
                title = 'Límite por restricción de flujo y óptima operación MPFM'
                titleXAxis = 'Porcentaje S&W'
                titleYAxis = 'API Seco'
                labelSeries1 = 'API Seco'
                labelSeries2 = 'Restricción por calidad'
                maxYValue = 30

                dataGraph.append(
                    {'x': str(i), series1: calculos.apiMezclaSeco, series2: 18})  # dict

            # ------------------------------------------graph4---------------------------------------------
            if graphId == "viscosidadBSW":
                # configurar para cada grafica
                series1 = 'referencia'
                series2 = 'viscosidadMezcla'
                title = 'Viscosidad del sistema'
                titleXAxis = 'Porcentaje S&W'
                titleYAxis = 'Viscosidad Mezcla cSt x % S&W '
                labelSeries1 = 'Viscosidad Transporte crudo cSt'
                labelSeries2 = 'Viscosidad Mezcla cSt'
                if(i == 0):
                    if(calculos.viscosidadMezcla>400):
                        maxYValue = round(calculos.viscosidadMezcla*1.05)
                    else:
                        maxYValue = 420

                dataGraph.append(
                    {'x': str(i), series1: 400, series2: calculos.viscosidadMezcla})  # dict

        grafica = Grafica(title=title,
                          titleXAxis=titleXAxis,
                          titleYAxis=titleYAxis,
                          maxYValue=maxYValue)
        grafica.addSerieParameters(serie=series1,
                                   label=labelSeries1,
                                   backgroundColor='rgb(100, 116, 254)',
                                   borderColor='rgb(100, 116, 254)',
                                   pointStyle='circle',
                                   pointRadius=3,
                                   pointBorderColor='rgb(125, 125, 125)')
        grafica.addSerieParameters(serie=series2,
                                   label=labelSeries2,
                                   backgroundColor='rgb(255, 99, 132)',
                                   borderColor='rgb(255, 99, 132)',
                                   pointStyle='star',
                                   pointRadius=3,
                                   pointBorderColor='rgb(125, 125, 125)')

        # return JsonResponse(diluyenteAInyectar, safe=False)# para list usar safe=false en el jsonresponse
        return JsonResponse({'datos': dataGraph, 'graphParams': grafica.getGraphParams(), 'contenedor': f"#{idContenedor}"})

    return render(request, "Basic/calculos.html")


@login_required(login_url="index")
def laboratorio_view(request):
    if request.method == "POST":
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            swMezcla = form.cleaned_data["swMezcla"]
            apiMezcla = form.cleaned_data["apiMezcla"]
            calculos = Calculos()
            calculos.calcularLaboratorio(apiMezcla, swMezcla)
            representation = Representations()
            data = representation.representacionLaboratorio(calculos)
            return render(request, "Basic/laboratorio.html", {
                "form": form,
                "esCalculado": True,
                "data": data
            })
        else:
            return render(request, "Basic/laboratorio.html", {
                "form": form
            })
    form = LaboratorioForm()
    return render(request, "Basic/laboratorio.html", {
        "form": form
    })


@login_required(login_url="index")
def pozoInyector_view(request):
    return render(request, "Basic/pozoInyector.html")


@login_required(login_url="index")
def dataHistorica_view(request):
    if request.method == "POST":
        form = DataHistoricaForm(request.POST)
        if form.is_valid():
            pozo = form.cleaned_data["pozo"]
            dataPozo = DataAVM.objects.filter(pozo=pozo).latest()
            representation = Representations()
            data = representation.representacionDataHistorica(dataPozo)
            return render(request, "Basic/dataHistorica.html", {
                "form": form,
                "data": data,
                "esCalculado": True
            })
    form = DataHistoricaForm()
    return render(request, "Basic/dataHistorica.html", {
        "form": form
    })


@login_required(login_url="index")
def cargarDatos(request):
    message = ''
    if request.method == 'POST':
        data_resource = DataAVMResource()
        dataset = Dataset()
        # print(f"dataset antes: {dataset}")
        datos_file = request.FILES['xlsfile']
        # print(f"datos_pozo: {datos_pozo}")
        imported_data = dataset.load(datos_file.read())
        # print(f"{dataset}")

        result = data_resource.import_data(
            dataset, dry_run=True)  # Test the data import
        if result.has_errors():
            message = f"Error al importar el archivo"
        else:
            message = 'Archivo cargado correctamente'
            data_resource.import_data(
                dataset, dry_run=False)  # Actually import now

    return render(request, 'Basic/cargarDatos.html', {
        "message": message
    })


@login_required(login_url="index")
def graficarDataHistorica_view(request, graphId):
    if request.method == "POST":
        data = json.loads(request.body)
        pozo = data.get("pozo")
        series = data["series"]
        idContenedor = data.get("idContenedor")
        dataGraph = []  # list

        dataPozo = DataAVM.objects.filter(pozo=pozo)

        if graphId == "historial":
            grafica = Grafica(title='Relación diluyente para API mezcla definido',
                              titleXAxis='Porcentaje S&W',
                              titleYAxis='Fracción volumétrica mezcla x % S&W cabeza')
            # ------------------------------------------graph1---------------------------------------------
            for i in range(99):
                # configurar para cada grafica
                series1 = 's&w'
                series2 = 'relacionOil_Diluyente'
                title = 'Relación diluyente para API mezcla definido'
                titleXAxis = 'Porcentaje S&W'
                titleYAxis = 'Fracción volumétrica mezcla x % S&W cabeza'
                labelSeries1 = 'Fracción Volumétrica de Agua de Mezcla'
                labelSeries2 = 'Relación Diluyente/Mezcla'
                maxYValue = 500

                dataGraph.append(
                    {'x': str(i), series1: 200, series2: 400})  # dict
        grafica = Grafica(title=title,
                          titleXAxis=titleXAxis,
                          titleYAxis=titleYAxis,
                          maxYValue=maxYValue)
        grafica.addSerieParameters(serie=series1,
                                   label=labelSeries1,
                                   backgroundColor='rgb(100, 116, 254)',
                                   borderColor='rgb(100, 116, 254)',
                                   pointStyle='circle',
                                   pointRadius=3,
                                   pointBorderColor='rgb(125, 125, 125)')
        grafica.addSerieParameters(serie=series2,
                                   label=labelSeries2,
                                   backgroundColor='rgb(255, 99, 132)',
                                   borderColor='rgb(255, 99, 132)',
                                   pointStyle='star',
                                   pointRadius=3,
                                   pointBorderColor='rgb(125, 125, 125)')

        return JsonResponse({'datos': dataGraph, 'graphParams': grafica.getGraphParams(), 'contenedor': f"#{idContenedor}"})

    return render(request, "Basic/calculos.html")
