import json


class Representations():

    def representacionDataHistorica(self, dataPozo):
        dataPozoRepresentation = {
            "fecha": dataPozo.fecha,
            "tablas": [{
                "titulo": "VARIABLES VARIADOR",
                "contenido": [{
                    "id": "Frecuencia",
                    "valor": dataPozo.velocidadBomba
                }, {
                    "id": "PIP",
                    "valor": dataPozo.pip
                }, {
                    "id": "Corriente",
                    "valor": dataPozo.corrienteVSD
                }]
            }, {
                "titulo": "VARIABLES SUPERFICIE",
                "contenido": [{
                    "id": "THP",
                    "valor": dataPozo.thp
                }, {
                    "id": "THT",
                    "valor": dataPozo.tempCabeza
                }]
            }, {
                "titulo": "CAUDALES",
                "contenido": [{
                    "id": "ACEITE BPD",
                    "valor": dataPozo.tasaAceite
                }, {
                    "id": "AGUA BPD",
                    "valor": dataPozo.tasaAgua
                }, {
                    "id": "FLUIDO BPD",
                    "valor": dataPozo.tasaLiquido
                }, {
                    "id": "GAS MSFCD",
                    "valor": dataPozo.tasaGas
                }]
            }, {
                "titulo": "PROPIEDADES",
                "contenido": [{
                    "id": "%S&W",
                    "valor": dataPozo.bsw
                }, {
                    "id": "API @60ºF",
                    "valor": dataPozo.api
                }, {
                    "id": "CLORUROS",
                    "valor": dataPozo.salinidad
                }, {
                    "id": "DILUYENTE",
                    "valor": None
                }]
            }, {
                "titulo": "COMENTARIOS",
                "contenido": dataPozo.comentarios
            }]
        }
        return dataPozoRepresentation

    # def representacionCalculos(self, dataPozo):
    #     dataPozoRepresentation = {
    #         "fecha": dataPozo.fecha,
    #         "tablas": [{
    #             "titulo": "VARIABLES VARIADOR",
    #             "contenido": [{
    #                 "id": "Frecuencia",
    #                 "valor": dataPozo.velocidadBomba
    #             }, {
    #                 "id": "PIP",
    #                 "valor": dataPozo.pip
    #             }, {
    #                 "id": "Corriente",
    #                 "valor": dataPozo.corrienteVSD
    #             }]
    #         }, {
    #             "titulo": "VARIABLES SUPERFICIE",
    #             "contenido": [{
    #                 "id": "THP",
    #                 "valor": dataPozo.thp
    #             }, {
    #                 "id": "THT",
    #                 "valor": dataPozo.tempCabeza
    #             }]
    #         }, {
    #             "titulo": "CAUDALES",
    #             "contenido": [{
    #                 "id": "ACEITE BPD",
    #                 "valor": dataPozo.tasaAceite
    #             }, {
    #                 "id": "AGUA BPD",
    #                 "valor": dataPozo.tasaAgua
    #             }, {
    #                 "id": "FLUIDO BPD",
    #                 "valor": dataPozo.tasaLiquido
    #             }, {
    #                 "id": "GAS MSFCD",
    #                 "valor": dataPozo.tasaGas
    #             }]
    #         }, {
    #             "titulo": "PROPIEDADES",
    #             "contenido": [{
    #                 "id": "%S&W",
    #                 "valor": dataPozo.bsw
    #             }, {
    #                 "id": "API @60ºF",
    #                 "valor": dataPozo.api
    #             }, {
    #                 "id": "CLORUROS",
    #                 "valor": dataPozo.salinidad
    #             }, {
    #                 "id": "DILUYENTE",
    #                 "valor": None
    #             }]
    #         }, {
    #             "titulo": "COMENTARIOS",
    #             "contenido": dataPozo.comentarios
    #         }]
    #     }
    #     return dataPozoRepresentation
