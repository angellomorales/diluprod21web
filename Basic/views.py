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
            if graphId == "relacionDiluyente":
                # configurar para cada grafica
                dataGraph.append(
                    {'x': str(i), 's&w': calculos.swMezcla, 'relacionOil_Diluyente': calculos.relacionOil_Diluyente})  # dict
                serieParams = {
                    's&w':
                    {
                        'label': 'Fracción Volumétrica de Agua de Mezcla',
                        'backgroundColor': 'rgb(100, 116, 254)',
                        'borderColor': 'rgb(100, 116, 254)',
                        'pointStyle': 'circle',
                        'pointRadius': 3
                    },
                    'relacionOil_Diluyente':
                    {
                        'label': 'Relación Diluyente/Mezcla',
                        'backgroundColor': 'rgb(255, 99, 132)',
                        'borderColor': 'rgb(255, 99, 132)',
                        'pointStyle': 'star',
                        'pointRadius': 3
                    }
                }
                graphParams = {
                    'title': 'Relación diluyente para API mezcla definido',
                    'titleXAxis': 'Porcentaje S&W',
                    'titleYAxis': 'Fracción volumétrica mezcla x % S&W cabeza',
                    'maxYValue': 1
                }
            if graphId == "diluyenteRequerido":
                # configurar para cada grafica
                dataGraph.append(
                    {'x': str(i), 'diluyente': calculos.diluyente, 'relacion1_3': calculos.relacion1_3})  # dict
                if(abs(calculos.diluyente-calculos.relacion1_3) < 20):
                    maxYValue = round(calculos.diluyente*2)
                serieParams = {
                    'diluyente':
                    {
                        'label': 'Diluyente A Inyectar',
                        'backgroundColor': 'rgb(100, 116, 254)',
                        'borderColor': 'rgb(100, 116, 254)',
                        'pointStyle': 'circle',
                        'pointRadius': 3
                    },
                    'relacion1_3':
                    {
                        'label': 'Relacion 1-3',
                        'backgroundColor': 'rgb(255, 99, 132)',
                        'borderColor': 'rgb(255, 99, 132)',
                        'pointStyle': 'star',
                        'pointRadius': 3
                    }
                }
                graphParams = {
                    'title': 'Diluyente Requerido para API mezcla definido',
                    'titleXAxis': 'Porcentaje S&W',
                    'titleYAxis': 'BPD',
                    'maxYValue': maxYValue
                }
            if graphId == "limiteRestriccion":
                # configurar para cada grafica
                dataGraph.append(
                    {'x': str(i), 'apiMezclaSeco': calculos.apiMezclaSeco, 'limiteSuperior': 18})  # dict
                serieParams = {
                    'apiMezclaSeco':
                    {
                        'label': 'API Seco',
                        'backgroundColor': 'rgb(100, 116, 254)',
                        'borderColor': 'rgb(100, 116, 254)',
                        'pointStyle': 'circle',
                        'pointRadius': 3
                    },
                    'limiteSuperior':
                    {
                        'label': 'Restricción por calidad',
                        'backgroundColor': 'rgb(255, 99, 132)',
                        'borderColor': 'rgb(255, 99, 132)',
                        'pointStyle': 'star',
                        'pointRadius': 3
                    }
                }
                graphParams = {
                    'title': 'Límite por restricción de flujo y óptima operación MPFM',
                    'titleXAxis': 'Porcentaje S&W',
                    'titleYAxis': 'API Seco',
                    'maxYValue': 30
                }
            if graphId == "viscosidadBSW":
                # configurar para cada grafica
                dataGraph.append(
                    {'x': str(i), 's&w': calculos.swMezcla, 'viscosidadMezcla': calculos.viscosidadMezcla})  # dict
                if(i == 0):
                    maxYValue = round(calculos.viscosidadMezcla*1.05)
                serieParams = {
                    's&w':
                    {
                        'label': 'Fracción Volumétrica de Agua de Mezcla',
                        'backgroundColor': 'rgb(100, 116, 254)',
                        'borderColor': 'rgb(100, 116, 254)',
                        'pointStyle': 'circle',
                        'pointRadius': 3
                    },
                    'viscosidadMezcla':
                    {
                        'label': 'Viscosidad Mezcla csp',
                        'backgroundColor': 'rgb(255, 99, 132)',
                        'borderColor': 'rgb(255, 99, 132)',
                        'pointStyle': 'star',
                        'pointRadius': 3
                    }
                }
                graphParams = {
                    'title': 'Viscosidad del sistema',
                    'titleXAxis': 'Porcentaje S&W',
                    'titleYAxis': 'Viscosidad Mezcla csp x % S&W ',
                    'maxYValue': maxYValue
                }

        # return JsonResponse(diluyenteAInyectar, safe=False)# para list usar safe=false en el jsonresponse
        return JsonResponse({'datos': dataGraph, 'serieParams': serieParams, 'graphParams': graphParams, 'contenedor': f"#{idContenedor}"})

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
    return render(request, "Basic/Laboratorio.html", {
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
