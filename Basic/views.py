import json
import decimal
from tablib import Dataset

from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import DataAVM, DataLaboratorio, Pozo, taskTracker, User
from .forms import CalculosForm, DataHistoricaForm, LaboratorioForm, CargarDatosForm
from .calculos import Calculos
from .resources import DataAVMResource, DataStorkResource, DataPozoInyectorResource, DataLaboratorioResource, DataPozoResource
from .representations import Representations
from .grafica import Grafica
from .tasks import import_data, import_data_task


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
    pozos = Pozo.objects.all()

    if request.method == "POST":
        form = CalculosForm(request.POST)
        if form.is_valid():
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
                "pozos": pozos,
                "esCalculado": True,
                "data": data,
                "diluyente": data.get('tablas')[1].get('contenido')[1].get('valor'),
                "api": data.get('tablas')[5].get('contenido')[0].get('valor')
            })
        else:
            # form.fields['category'].choices = CategoryChoices.choices#add a choices in category
            return render(request, "Basic/calculos.html", {
                "form": form,
                "pozos": pozos
            })
    form = CalculosForm()
    return render(request, "Basic/calculos.html", {
        "form": form,
        "pozos": pozos
    })


@login_required(login_url="index")
def cargarPredataCalculos_view(request, pozoId):
    if request.method == "POST":
        try:
            dataAVM = DataAVM.objects.filter(pozo=pozoId).exclude(
                pruebaValida="PENDIENTE").latest()
            representations = Representations()
            dataResponse = {
                'pozoId': pozoId, 'data': representations.representacionDataHistorica(dataAVM)}
            return JsonResponse(dataResponse)
        except DataAVM.DoesNotExist:
            return JsonResponse({'pozoId': None})
    return render(request, "Basic/calculos.html")


@login_required(login_url="index")
def graficarCalculos_view(request, graphId):
    if request.method == "POST":
        data = json.loads(request.body)
        calculos = Calculos()
        aceite = data["aceite"]
        apiCabeza = data["apiCabeza"]
        apiDiluyente = data.get("apiDiluyente")
        variableACalcular = data.get("apiMezclaHumedo")
        idContenedor = data.get("idContenedor")
        grafica = Grafica()
        series = []
        representation = Representations()

        for i in range(99):
            calculos.calcularDiluyente(
                apiCabeza, apiDiluyente, variableACalcular, aceite, i, False)
            dataSerie = representation.representacionGraficasCalculos(calculos)

            # configurar para cada grafica
            series = dataSerie.get(f"{graphId}")['series']
            title = dataSerie.get(f"{graphId}")['title']
            titleXAxis = dataSerie.get(f"{graphId}")['titleXAxis']
            titleYAxis = dataSerie.get(f"{graphId}")['titleYAxis']
            maxYValue = dataSerie.get(f"{graphId}")['maxYValue']

            if graphId == "diluyenteRequerido":
                if(abs(calculos.diluyente-calculos.relacion1_3) < 20):
                    maxYValue = round(calculos.diluyente*2)
            if graphId == "viscosidadBSW":
                if(i == 0):
                    if(calculos.viscosidadMezcla > 400):
                        maxYValue = round(calculos.viscosidadMezcla*1.05)
                    else:
                        maxYValue = 420

            datos = {'x': str(i)}

            # ---------------------------construccion de data--------------------------------
            for serie in series:
                datos[serie['nombre']] = serie['variable']
            grafica.addSeriesData(**datos)  # dict

        # --------------------------------construccion de grafica----------------------------
        grafica.addParameters(title=title,
                              titleXAxis=titleXAxis,
                              titleYAxis=titleYAxis,
                              maxYValue=maxYValue)
        for ser in series:
            grafica.addSerieParameters(serie=ser['nombre'],
                                       label=ser['label'],
                                       backgroundColor=ser['backgroundColor'],
                                       borderColor=ser['borderColor'],
                                       pointStyle=ser['pointStyle'],
                                       pointRadius=3,
                                       pointBorderColor='rgb(125, 125, 125)')

        # return JsonResponse(diluyenteAInyectar, safe=False)# para list usar safe=false en el jsonresponse
        return JsonResponse({'datos': grafica.dataGraph, 'graphParams': grafica.getGraphParams(), 'contenedor': f"#{idContenedor}"})

    return render(request, "Basic/calculos.html")


@login_required(login_url="index")
def laboratorio_view(request):
    pozos = Pozo.objects.all()
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
                "pozos": pozos,
                "data": data
            })
        else:
            return render(request, "Basic/laboratorio.html", {
                "form": form,
                "pozos": pozos,
            })
    form = LaboratorioForm()
    return render(request, "Basic/laboratorio.html", {
        "form": form,
        "pozos": pozos,
    })


@login_required(login_url="index")
def cargarTablaLaboratorio_view(request, pozoId):
    if request.method == "POST":
        data = []
        try:
            dataLab = DataLaboratorio.objects.filter(pozo=pozoId)
            representations = Representations()
            for item in dataLab:
                data.append(
                    representations.representacionDataLaboratorio(item))
            return JsonResponse({'datos': data})
        except DataLaboratorio.DoesNotExist:
            return JsonResponse({'datos': None})
    return render(request, "Basic/Laboratorio.html")


@login_required(login_url="index")
def pozoInyector_view(request):
    return render(request, "Basic/pozoInyector.html")


@login_required(login_url="index")
def dataHistorica_view(request):
    pozos = Pozo.objects.all()

    if request.method == "POST":
        form = DataHistoricaForm(request.POST)
        if form.is_valid():
            try:
                pozo = form.cleaned_data["pozo"]
                dataPozo = DataAVM.objects.filter(pozo=pozo).exclude(
                    pruebaValida="PENDIENTE").latest()
                representation = Representations()
                data = representation.representacionDataHistorica(dataPozo)
                return render(request, "Basic/dataHistorica.html", {
                    "form": form,
                    "data": data,
                    "pozos": pozos,
                    "esCalculado": True
                })
            except DataAVM.DoesNotExist:
                return render(request, "Basic/dataHistorica.html", {
                    "form": form,
                    "pozos": pozos,
                })

    form = DataHistoricaForm()
    return render(request, "Basic/dataHistorica.html", {
        "form": form,
        "pozos": pozos,
    })


@login_required(login_url="index")
def cargarDatos(request):
    taskTracker = taskStatus()

    if request.method == 'POST':

        form = CargarDatosForm(request.POST, request.FILES)
        if form.is_valid():
            tipo = request.POST['tipo']
            if tipo == 'Data AVM':
                data_resource = DataAVMResource()
            if tipo == 'Data Stork':
                data_resource = DataStorkResource()
            if tipo == 'Data Pozo Inyector':
                data_resource = DataPozoInyectorResource()
            if tipo == 'Data Laboratorio':
                data_resource = DataLaboratorioResource()
            dataset = Dataset()
            # print(f"dataset antes: {dataset}")
            datos_file = request.FILES['archivo']
            # print(f"datos_pozo: {datos_pozo}")
            dataset.load(datos_file.read())
            # print(f"{dataset}")

            import_data_task.delay(data_resource, dataset)
            # import_data(data_resource, dataset)
            return HttpResponseRedirect(reverse("index"))
    form = CargarDatosForm()

    return render(request, "Basic/cargarDatos.html", {
        "taskTracker": taskTracker,
        "form": form
    })


def taskStatus():
    task = taskTracker.objects.filter(task=import_data_task.__name__)
    if task.exists():
        return(task.get())
    else:
        return None


@login_required(login_url="index")
def graficarDataHistorica_view(request, graphId):
    if request.method == "POST":
        data = json.loads(request.body)
        pozo = data.get("pozo")
        dataPozo = DataAVM.objects.filter(pozo=pozo)
        return graficarHistorico(data,dataPozo,graphId)
    return render(request, "Basic/calculos.html")

@login_required(login_url="index")
def graficarTablaLaboratorio_view(request, graphId):
    if request.method == "POST":
        data = json.loads(request.body)
        pozo = data.get("pozo")
        dataPozo = DataLaboratorio.objects.filter(pozo=pozo)
        return graficarHistorico(data,dataPozo,graphId,isLab=True)
    return render(request, "Basic/Laboratorio.html")


def graficarHistorico(data, dataPozo, graphId,**kwargs):
    idSeries = data["series"]
    idContenedor = data.get("idContenedor")
    grafica = Grafica()
    series = []
    maxYValue = 100

    # ------------------------------------------graph1---------------------------------------------
    for item in dataPozo:
        if graphId == "historial":
            # configurar para cada grafica
            for idSerie in idSeries:
                # stringLabel=''.join( x for x in idSerie if x not in "id_")
                if('isLab' in kwargs):
                    variable=item.__dict__.get(idSerie['id'])
                else:
                    variable=getVariable_AVM_or_Stork(item, idSerie)
                series.append({
                    'nombre': idSerie['id'],
                    'variable': variable,
                    'label': f"{idSerie['label']} ({idSerie['unidades']})",
                    'backgroundColor': idSerie['color'],
                    'borderColor': idSerie['color'],
                    'pointStyle': 'circle'
                })
            title = 'Histórico de datos'
            titleXAxis = 'Tiempo'
            titleYAxis = ''

        datos = {'x': str(item.fecha)}

        # ---------------------------construccion de data--------------------------------
        for serie in series:
            datos[serie['nombre']] = serie['variable']
            if not (serie['variable'] == None):
                if maxYValue < serie['variable']*decimal.Decimal(1.05):
                    maxYValue = round(
                        serie['variable']*decimal.Decimal(1.05))
        grafica.addSeriesData(**datos)  # dict

    # --------------------------------construccion de grafica----------------------------
    grafica.addParameters(title=title,
                          titleXAxis=titleXAxis,
                          titleYAxis=titleYAxis,
                          maxYValue=maxYValue)
    for ser in series:
        grafica.addSerieParameters(serie=ser['nombre'],
                                   label=ser['label'],
                                   backgroundColor=ser['backgroundColor'],
                                   borderColor=ser['borderColor'],
                                   pointStyle=ser['pointStyle'],
                                   pointRadius=3,
                                   pointBorderColor='rgb(125, 125, 125)')

    # return JsonResponse(diluyenteAInyectar, safe=False)# para list usar safe=false en el jsonresponse
    return JsonResponse({'datos': grafica.dataGraph, 'graphParams': grafica.getGraphParams(), 'contenedor': f"#{idContenedor}"})


def getVariable_AVM_or_Stork(item, idSerie):

    datastork = item.storkAVM.all().get() if item.storkAVM.all().exists() else None

    if item.__dict__.get(idSerie['id']):
        return item.__dict__.get(idSerie['id'])
    else:
        return getattr(datastork, idSerie['id'], None)


@login_required(login_url="index")
def pozoNuevo_view(request):
    msg = None
    if request.method == "POST":
        msg = None
    return render(request, "Basic/pozoNuevo.html", {
        "message": msg
    })
