from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields.mixins import FieldCacheMixin


class User(AbstractUser):
    pass


class taskTracker(models.Model):
    CHOICESSTATUS = [('FINISHED', 'FINISHED'),
                     ('WORKING', 'WORKING'),
                     ('FAILED', 'FAILED')]
    task = models.CharField(
        max_length=255, primary_key=True, blank=False, null=False)
    task_id = models.CharField(max_length=255)
    status = models.CharField(
        max_length=12, choices=CHOICESSTATUS, default='FINISHED', blank=False, null=False)
    type_error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.task} status: {self.status}"


class Campo(models.Model):
    nombre = models.CharField(max_length=255)
    pozos = models.ManyToManyField(
        'Pozo', blank=True, related_name="ListaPozos")

    def __str__(self):
        return f"{self.nombre}"


class Pozo(models.Model):
    CHOICES = [('Activo', 'Activo'),
               ('Inactivo', 'Inactivo')]
    nombre = models.CharField(
        max_length=255, primary_key=True, blank=False, null=False)
    estado = models.CharField(
        max_length=8, choices=CHOICES, default='Inactivo', blank=False, null=False)
    latitud = models.DecimalField(
        max_digits=6, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(
        max_digits=6, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}"


class DataAVM(models.Model):
    CHOICES = [('VALIDA', 'Valida'),
               ('PENDIENTE', 'Pendiente')]
    campo = models.ForeignKey(
        Campo, on_delete=models.CASCADE, blank=True, null=True)
    pozo = models.ForeignKey(
        Pozo, on_delete=models.CASCADE, related_name='PozoDataAVM')
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    bsw = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    api = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    tasaLiquido = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    tasaGas = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    tasaAgua = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    tasaAceite = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    gor = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    thp = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    velocidadBomba = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    corrienteVSD = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    pip = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    voltajeOutVSD = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    tempCabeza = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    pruebaValida = models.CharField(
        max_length=10, choices=CHOICES, default='VALIDA', blank=False)
    comentarios = models.TextField(blank=True, null=True)
    salinidad = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.fecha}: {self.pozo} Fluido Total: {self.tasaLiquido} S&W: {self.bsw}"

    class Meta:
        ordering = ["fecha"]
        get_latest_by = "fecha"


class DataStork(models.Model):
    dataAVM = models.ForeignKey(
        DataAVM, on_delete=models.CASCADE, related_name="storkAVM")
    medidorNo = models.IntegerField(blank=True, null=True)
    noWell = models.CharField(max_length=20, blank=True, null=True)
    swMezcla = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    diluyenteInyectado = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    fluidoTotal = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    bsw = models.DecimalField(
        max_digits=11, decimal_places=3, blank=True, null=True)
    api = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
            return f"{self.dataAVM}:  | Fluido total stok: {self.fluidoTotal} S&W stork: {self.bsw*100}"


class DataAgar(models.Model):
    dataAVM = models.ForeignKey(
        DataAVM, on_delete=models.CASCADE, related_name="agarAVM")
    medidorNo = models.IntegerField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
