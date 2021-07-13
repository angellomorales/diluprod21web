import json


class Representations():

    def representacionDataHistorica(self, dataPozo):
        dataPozoRepresentation = {
            "fecha": dataPozo.fecha,
            "tablas": [{
                "titulo": "VARIABLES VARIADOR",
                "contenido": [{
                    "id": "id_frecuencia",
                    "cabecera": "Frecuencia",
                    "valor": dataPozo.velocidadBomba
                }, {
                    "id": "id_pip",
                    "cabecera": "PIP",
                    "valor": dataPozo.pip
                }, {
                    "id": "id_corriente",
                    "cabecera": "Corriente",
                    "valor": dataPozo.corrienteVSD
                }]
            }, {
                "titulo": "VARIABLES SUPERFICIE",
                "contenido": [{
                    "id": "id_thp",
                    "cabecera": "THP",
                    "valor": dataPozo.thp
                }, {
                    "id": "id_tht",
                    "cabecera": "THT",
                    "valor": dataPozo.tempCabeza
                }]
            }, {
                "titulo": "CAUDALES",
                "contenido": [{
                    "id": "id_aceite",
                    "cabecera": "ACEITE BPD",
                    "valor": dataPozo.tasaAceite
                }, {
                    "id": "id_agua",
                    "cabecera": "AGUA BPD",
                    "valor": dataPozo.tasaAgua
                }, {
                    "id": "id_liquido",
                    "cabecera": "FLUIDO BPD",
                    "valor": dataPozo.tasaLiquido
                }, {
                    "id": "id_gas",
                    "cabecera": "GAS MSFCD",
                    "valor": dataPozo.tasaGas
                }]
            }, {
                "titulo": "PROPIEDADES",
                "contenido": [{
                    "id": "id_bsw",
                    "cabecera": "%S&W",
                    "valor": dataPozo.bsw
                }, {
                    "id": "id_api",
                    "cabecera": "API @60ºF",
                    "valor": dataPozo.api
                }, {
                    "id": "id_cloruros",
                    "cabecera": "CLORUROS",
                    "valor": dataPozo.salinidad
                }, {
                    "id": "id_diluyente",
                    "cabecera": "DILUYENTE",
                    "valor": None
                }]
            }, {
                "titulo": "COMENTARIOS",
                "contenido": [{
                    "id": "id_comentarios",
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
                "titulo": "VISCOSIDAD cSt",
                "contenido": [{
                    "cabecera": "Aceite",
                    "valor": calculos.viscosidadAceite,
                },{
                    "cabecera": "Diluyente",
                    "valor": calculos.viscosidadDiluyente,
                },{
                    "cabecera": "Mezcla",
                    "valor": calculos.viscosidadMezcla,
                },{
                    "cabecera": "Agua",
                    "valor": calculos.viscosidadAgua,
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
