from Basic.calculos import NewCalculos
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import NewCalculosForm
from .calculos import NewCalculos


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
        form = NewCalculosForm(request.POST)
        if form.is_valid():
            aceite = form.cleaned_data["aceitePruebaAnterior"]
            swCabeza = form.cleaned_data["fraccionSYWCabeza"]
            apiCabeza = form.cleaned_data["APICabeza"]
            apiDiluyente = form.cleaned_data["APIDiluyente"]
            tipoCalculo = form.cleaned_data["tipoCalculo"]
            variableACalcular = form.cleaned_data["variableACalcular"]
            calculos= NewCalculos()
            calculos.calcularDiluyente(apiCabeza,apiDiluyente,variableACalcular,aceite,swCabeza,True)
            return render(request, "Basic/calculos.html", {
                "form": form,
                "esCalculado": True,
                "calculos":calculos
            })
        else:
            # form.fields['category'].choices = CategoryChoices.choices#add a choices in category
            return render(request, "Basic/calculos.html", {
                "form": form
            })
    form = NewCalculosForm()
    return render(request, "Basic/calculos.html", {
        "form": form
    })
