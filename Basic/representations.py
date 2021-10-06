import json


class Representations():

    def representacionDataHistorica(self, dataPozo):
        # traer la data stork relacionada a data avm si existe ver modelo
        datastork = dataPozo.storkAVM.all().get(
        ) if dataPozo.storkAVM.all().exists() else None
        dataPozoRepresentation = {
            "fecha": dataPozo.fecha,
            "tablas": [{
                "titulo": "VARIABLES VARIADOR",
                "contenido": [{
                    "id": "velocidadBomba",
                    "cabecera": "Frecuencia",
                    "valor": dataPozo.velocidadBomba,
                    "unidades": "Hz",
                    "color": "rgb(100, 116, 254)"  # Azul
                }, {
                    "id": "pip",
                    "cabecera": "PIP",
                    "valor": dataPozo.pip,
                    "unidades": "Psi",
                    "color": "rgb(255, 99, 132)"  # rojo claro
                }, {
                    "id": "corrienteVSD",
                    "cabecera": "Corriente",
                    "valor": dataPozo.corrienteVSD,
                    "unidades": "A",
                    "color": "rgb(96, 249, 33)"  # Verde
                }]
            }, {
                "titulo": "VARIABLES SUPERFICIE",
                "contenido": [{
                    "id": "thp",
                    "cabecera": "THP",
                    "valor": dataPozo.thp,
                    "unidades": "Psi",
                    "color": "rgb(241, 255, 99)"  # Amarillo
                }, {
                    "id": "tempCabeza",
                    "cabecera": "THT",
                    "valor": dataPozo.tempCabeza,
                    "unidades": "ºF",
                    "color": "rgb(248, 99, 255)"  # Purpura
                }]
            }, {
                "titulo": "CAUDALES",
                "contenido": [{
                    "id": "tasaAceite",
                    "cabecera": "ACEITE BPD",
                    "valor": dataPozo.tasaAceite,
                    "unidades": "BPD",
                    "color": "rgb(152, 115, 101)"  # Cafe
                }, {
                    "id": "tasaAgua",
                    "cabecera": "AGUA BPD",
                    "valor": dataPozo.tasaAgua,
                    "unidades": "BPD",
                    "color": "rgb(133, 221, 255)"  # Azul claro
                }, {
                    "id": "tasaLiquido",
                    "cabecera": "FLUIDO BPD",
                    "valor": dataPozo.tasaLiquido,
                    "unidades": "BPD",
                    "color": "rgb(235, 138, 57)"  # Naranja
                }, {
                    "id": "tasaGas",
                    "cabecera": "GAS MSFCD",
                    "valor": dataPozo.tasaGas,
                    "unidades": "MSFCD",
                    "color": "rgb(167, 164, 161)"  # Gris
                }]
            }, {
                "titulo": "PROPIEDADES",
                "contenido": [{
                    "id": "bsw",
                    "cabecera": "%S&W",
                    "valor": dataPozo.bsw,
                    "unidades": "%",
                    "color": "rgb(160, 227, 201)"  # Aguamarina
                }, {
                    "id": "api",
                    "cabecera": "API @60ºF",
                    "valor": dataPozo.api,
                    "unidades": "",
                    "color": "rgb(43, 81, 92)"  # Azul-Negro
                }, {
                    "id": "salinidad",
                    "cabecera": "CLORUROS",
                    "valor": dataPozo.salinidad,
                    "unidades": "Ppm",
                    "color": "rgb(170, 145, 13)"  # Amarillo quemado
                }, {
                    "id": "diluyenteInyectado",
                    "cabecera": "DILUYENTE",
                    "valor": getattr(datastork, 'diluyenteInyectado', None),
                    "unidades": "BPD",
                    "color": "rgb(179, 242, 216)"  # Verde Crema
                }, {
                    "id": "swMezcla",
                    "cabecera": "S&W Mezcla",
                    "valor": getattr(datastork, 'swMezcla', None),
                    "unidades": "%",
                    "color": "rgb(197, 170, 198)"  # rosado quemado
                }, {
                    "id": "apiMezcla",
                    "cabecera": "API Mezcla",
                    "valor": getattr(datastork, 'apiMezcla', None),
                    "unidades": "º",
                    "color": "rgb(172, 198, 242)"  # Azul Crema
                }]
            }, {
                "titulo": "COMENTARIOS",
                "contenido": [{
                    "id": "comentarios",
                    "valor": (f"{dataPozo.comentarios} \n{getattr(datastork,'comentarios','')}")
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
                }, {
                    "cabecera": "Diluyente",
                    "valor": calculos.viscosidadDiluyente,
                }, {
                    "cabecera": "Mezcla",
                    "valor": calculos.viscosidadMezcla,
                }, {
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

    def representacionGraficasCalculos(self, calculos):
        representation = {
            'relacionDiluyente': {
                'series': [{
                    'nombre': 's&w',
                    'variable': calculos.swMezcla,
                    'label': 'Fracción Volumétrica de Agua de Mezcla',
                    'backgroundColor': 'rgb(100, 116, 254)',
                    'borderColor': 'rgb(100, 116, 254)',
                    'pointStyle': 'circle',
                }, {
                    'nombre': 'relacionOil_Diluyente',
                    'variable': calculos.relacionOil_Diluyente,
                    'label': 'Relación Diluyente/Mezcla',
                    'backgroundColor': 'rgb(255, 99, 132)',
                    'borderColor': 'rgb(255, 99, 132)',
                    'pointStyle': 'star',
                }],
                'title': 'Relación diluyente para API mezcla definido',
                'titleXAxis': 'Porcentaje S&W',
                'titleYAxis': 'Fracción volumétrica mezcla x % S&W cabeza',
                'maxYValue': 1
            },
            'diluyenteRequerido': {
                'series': [{
                    'nombre': 'diluyente',
                    'variable': calculos.diluyente,
                    'label': 'Diluyente A Inyectar',
                    'backgroundColor': 'rgb(100, 116, 254)',
                    'borderColor': 'rgb(100, 116, 254)',
                    'pointStyle': 'circle',
                }, {
                    'nombre': 'relacion1_3',
                    'variable': calculos.relacion1_3,
                    'label': 'Relacion 1-3',
                    'backgroundColor': 'rgb(255, 99, 132)',
                    'borderColor': 'rgb(255, 99, 132)',
                    'pointStyle': 'star',
                }],
                'title': 'Diluyente Requerido para API mezcla definido',
                'titleXAxis': 'Porcentaje S&W',
                'titleYAxis': 'BPD',
                'maxYValue': calculos.relacion1_3*2.5
            },
            'limiteRestriccion': {
                'series': [{
                    'nombre': 'apiMezclaSeco',
                    'variable': calculos.apiMezclaSeco,
                    'label': 'API Seco',
                    'backgroundColor': 'rgb(100, 116, 254)',
                    'borderColor': 'rgb(100, 116, 254)',
                    'pointStyle': 'circle',
                }, {
                    'nombre': 'limiteSuperior',
                    'variable': 16,
                    'label': 'Restricción por calidad superior',
                    'backgroundColor': 'rgb(255, 99, 132)',
                    'borderColor': 'rgb(255, 99, 132)',
                    'pointStyle': 'star',
                }, {
                    'nombre': 'limiteInferior',
                    'variable': 13,
                    'label': 'Restricción por calidad inferior',
                    'backgroundColor': 'rgb(96, 249, 33)',
                    'borderColor': 'rgb(96, 249, 33)',
                    'pointStyle': 'crossRot',
                }],
                'title': 'Límite por restricción de flujo y óptima operación MPFM',
                'titleXAxis': 'Porcentaje S&W',
                'titleYAxis': 'API Seco',
                'maxYValue': 30
            },
            'viscosidadBSW': {
                'series': [{
                    'nombre': 'referencia',
                    'variable': 400,
                    'label': 'Viscosidad Transporte crudo cSt',
                    'backgroundColor': 'rgb(100, 116, 254)',
                    'borderColor': 'rgb(100, 116, 254)',
                    'pointStyle': 'circle',
                }, {
                    'nombre': 'viscosidadMezcla',
                    'variable': calculos.viscosidadMezcla,
                    'label': 'Viscosidad Mezcla cSt',
                    'backgroundColor': 'rgb(255, 99, 132)',
                    'borderColor': 'rgb(255, 99, 132)',
                    'pointStyle': 'star',
                }],
                'title': 'Viscosidad del sistema',
                'titleXAxis': 'Porcentaje S&W',
                'titleYAxis': 'Viscosidad Mezcla cSt x % S&W ',
                'maxYValue': 420
            }
        }
        return representation
