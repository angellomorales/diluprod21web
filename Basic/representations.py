import json


class Representations():

    def representacionDataHistorica(self, dataPozo):
        dataPozoRepresentation = {
            "fecha": dataPozo.fecha,
            "tablas": [{
                "titulo": "VARIABLES VARIADOR",
                "contenido": [{
                    "cabecera": "Frecuencia",
                    "valor": dataPozo.velocidadBomba
                }, {
                    "cabecera": "PIP",
                    "valor": dataPozo.pip
                }, {
                    "cabecera": "Corriente",
                    "valor": dataPozo.corrienteVSD
                }]
            }, {
                "titulo": "VARIABLES SUPERFICIE",
                "contenido": [{
                    "cabecera": "THP",
                    "valor": dataPozo.thp
                }, {
                    "cabecera": "THT",
                    "valor": dataPozo.tempCabeza
                }]
            }, {
                "titulo": "CAUDALES",
                "contenido": [{
                    "cabecera": "ACEITE BPD",
                    "valor": dataPozo.tasaAceite
                }, {
                    "cabecera": "AGUA BPD",
                    "valor": dataPozo.tasaAgua
                }, {
                    "cabecera": "FLUIDO BPD",
                    "valor": dataPozo.tasaLiquido
                }, {
                    "cabecera": "GAS MSFCD",
                    "valor": dataPozo.tasaGas
                }]
            }, {
                "titulo": "PROPIEDADES",
                "contenido": [{
                    "cabecera": "%S&W",
                    "valor": dataPozo.bsw
                }, {
                    "cabecera": "API @60ºF",
                    "valor": dataPozo.api
                }, {
                    "cabecera": "CLORUROS",
                    "valor": dataPozo.salinidad
                }, {
                    "cabecera": "DILUYENTE",
                    "valor": None
                }]
            }, {
                "titulo": "COMENTARIOS",
                "contenido": [{
                    "valor": dataPozo.comentarios
                }]
            }]
        }
        return dataPozoRepresentation

    def representacionCalculos(self, calculos):
        representation = {
            "tablas": [{
                "titulo": "GENERAL",
                "contenido": [{
                    "cabecera": "fracción S&W de Mezcla",
                    "valor": calculos.swMezcla
                }, {
                    "cabecera": "Relación Diluyente/Mezcla",
                    "valor": calculos.relacionOil_Diluyente
                }, {
                    "cabecera": "% Factor de encogimiento",
                    "valor": calculos.factorEncogimiento
                }]
            }, {
                "titulo": "CAUDALES BPD",
                "contenido": [{
                    "cabecera": "Aceite Qo",
                    "valor": calculos.aceite
                }, {
                    "cabecera": "Diluyente Qd",
                    "valor": calculos.diluyente
                }, {
                    "cabecera": "Agua Qw",
                    "valor": calculos.agua
                }]
            }, {
                "titulo": "GRAVEDAD ESPECIFICA @ 60ºF",
                "contenido": [{
                    "cabecera": "Aceite Cabeza",
                    "valor": calculos.geAceite
                }, {
                    "cabecera": "Diluyente",
                    "valor": calculos.geDiluyente
                }, {
                    "cabecera": "Mezcla",
                    "valor": calculos.geMezclaSeco
                }, {
                    "cabecera": "Agua",
                    "valor": 1
                }, {
                    "cabecera": "Líquido",
                    "valor": calculos.geLiquido
                }]
            }, {
                "titulo": "API @ 60ºF",
                "contenido": [{
                    "cabecera": "Mezcla",
                    "valor": calculos.apiMezclaSeco,
                }, {
                    "td_id": "id_apiMezclaHumedo",
                    "cabecera": "Líquido",
                    "valor": calculos.apiMezclaHumedo
                }]
            }, {
                "titulo": "DENSIDAD lb/ft <sup>3</sup>",
                "contenido": [{
                    "cabecera": "Mezcla",
                    "valor": calculos.densidadEmulsion
                }, {
                    "cabecera": "Diluyente",
                    "valor": calculos.densidadDiluyente
                }, {
                    "cabecera": "Líquido",
                    "valor": calculos.densidadLiquido
                }]
            }]
        }
        return representation

    def representacionLaboratorio(self, calculos):
        representation = {
            "tablas": [{
                "titulo": "GRAVEDAD ESPECIFICA @ 60ºF",
                "contenido": [{
                    "cabecera": "Mezcla",
                    "valor": calculos.geMezclaSeco
                }, {
                    "cabecera": "Agua",
                    "valor": 1
                }, {
                    "cabecera": "Líquido",
                    "valor": calculos.geLiquido
                }]
            }, {
                "titulo": "API @ 60ºF",
                "contenido": [{
                    "cabecera": "Mezcla",
                    "valor": calculos.apiMezclaSeco,
                }, {
                    "cabecera": "Líquido",
                    "valor": calculos.apiMezclaHumedo
                }]
            }, {
                "titulo": "DENSIDAD lb/ft <sup>3</sup>",
                "contenido": [{
                    "cabecera": "Mezcla",
                    "valor": calculos.densidadEmulsion
                }, {
                    "cabecera": "Agua",
                    "valor": calculos.densidadAgua
                }, {
                    "cabecera": "Líquido",
                    "valor": calculos.densidadLiquido
                }]
            }]
        }
        return representation
