from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import *


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
            aceitePruebaAnterior = form.cleaned_data["aceitePruebaAnterior"]
            fraccionSYWCabeza = form.cleaned_data["fraccionSYWCabeza"]
            APICabeza = form.cleaned_data["APICabeza"]
            APIDiluyente = form.cleaned_data["APIDiluyente"]
            TipoCalculo = form.cleaned_data["TipoCalculo"]
            return HttpResponseRedirect(reverse("index"))
        else:
            # form.fields['category'].choices = CategoryChoices.choices#add a choices in category
            return render(request, "Basic/calculos.html", {
                "form": form
            })
    form = NewCalculosForm()
    return render(request, "Basic/calculos.html", {
        "form": form
    })

