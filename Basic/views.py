import json
from django.http.response import JsonResponse
from Basic.calculos import Calculos
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import CalculosForm
from .calculos import Calculos


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
            return render(request, "Basic/calculos.html", {
                "form": form,
                "esCalculado": True,
                "calculos": calculos
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
def graficas_view(request, graphId):
    if request.method == "POST":
        data = json.loads(request.body)
        calculos = Calculos()
        pozo = data.get("pozo")
        aceite = data["aceite"]
        apiCabeza = data["apiCabeza"]
        apiDiluyente = data.get("apiDiluyente")
        variableACalcular = data.get("apiMezclaHumedo")
        dataGraph={}
        diluyenteAInyectar = []
        # diluyenteAInyectar = {}
        for i in range(99):
            sw = i*0.01
            calculos.calcularDiluyente(
                apiCabeza, apiDiluyente, variableACalcular, aceite, sw, False)
            diluyenteAInyectar.append(calculos.diluyente)# para list usar safe=false en el jsonresponse
            # diluyenteAInyectar[i]=calculos.diluyente
        if graphId == "relacionDiluyente":
            return JsonResponse(diluyenteAInyectar, safe=False)
            # return JsonResponse(diluyenteAInyectar)

    return render(request, "Basic/calculos.html")
