from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("calculos", views.calculos_view, name="calculos"),
    path("laboratorio", views.laboratorio_view, name="laboratorio"),
    path("pozoInyector", views.pozoInyector_view, name="pozoInyector"),
    path("dataHistorica", views.dataHistorica_view, name="dataHistorica"),
    path("cargarDatos", views.cargarDatos, name="cargarDatos"),
    path("graficarCalculos/<str:graphId>", views.graficarCalculos_view, name="graficarCalculos"),
    path("graficarDataHistorica/<str:graphId>", views.graficarDataHistorica_view, name="graficarDataHistorica"),
]
