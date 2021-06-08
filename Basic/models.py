from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields.mixins import FieldCacheMixin


class User(AbstractUser):
    pass


class Campo(models.Model):
    nombre = models.CharField(max_length=255)
    pozos = models.ManyToManyField(
        'Pozo', blank=True, related_name="ListaPozos")


class Pozo(models.Model):
    CHOICES = [('ACTIVE', 'Activo'),
               ('INACTIVE', 'Inactivo')]
    nombre = models.CharField(max_length=255)
    latitud = models.DecimalField(max_digits=6, decimal_places=6, blank=True)
    longitud = models.DecimalField(max_digits=6, decimal_places=6, blank=True)
    estado = models.CharField(
        max_length=8, choices=CHOICES, default='ACTIVE', blank=False)


class DataAVM(models.Model):
    CHOICES = [('VALIDA', 'Valida'),
               ('PENDIE', 'Pendiente')]
    pozo = models.ForeignKey(Pozo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    bsw = models.DecimalField(max_digits=7, decimal_places=2)
    api = models.DecimalField(max_digits=7, decimal_places=2)
    tasaLiquido = models.DecimalField(max_digits=11, decimal_places=2)
    tasaGas = models.DecimalField(max_digits=11, decimal_places=2)
    tasaAgua = models.DecimalField(max_digits=11, decimal_places=2)
    tasaAceite = models.DecimalField(max_digits=11, decimal_places=2)
    gor = models.DecimalField(max_digits=7, decimal_places=2)
    thp = models.DecimalField(max_digits=11, decimal_places=2)
    velocidadBomba = models.DecimalField(max_digits=7, decimal_places=2)
    corrienteVSD = models.DecimalField(max_digits=7, decimal_places=2)
    pip = models.DecimalField(max_digits=11, decimal_places=2)
    voltajeOutVSD = models.DecimalField(max_digits=7, decimal_places=2)
    tempCabeza = models.DecimalField(max_digits=7, decimal_places=2)
    pruebaValida = models.CharField(
        max_length=6, choices=CHOICES, default='VALIDA', blank=False)
    comentarios = models.TextField()
    salinidad = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.fecha}: {self.pozo} Fluido Total: {self.tasaLiquido} Estado: {self.pruebaValida}"


class DataStork(models.Model):
    dataAVM = models.ForeignKey(
        DataAVM, on_delete=models.CASCADE, related_name="storkAVM", blank=True)
    medidorNo = models.IntegerField(blank=True)
    noWell = models.CharField(max_length=20, blank=True)
    swMezcla = models.DecimalField(max_digits=11, decimal_places=2, blank=True)
    diluyenteInyectado = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True)
    comentarios = models.TextField(blank=True)


class DataAgar(models.Model):
    dataAVM = models.ForeignKey(
        DataAVM, on_delete=models.CASCADE, related_name="agarAVM", blank=True)
    reporte = models.IntegerField(blank=True)
