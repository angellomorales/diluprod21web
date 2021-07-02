class Representations():
    def representacionDataHistoricaJSON(dataPozo):
        dataPozoRepresentation = {
            "tablas": [{
                "titulo": "VARIABLES VARIADOR",
                "contenido": [{
                    "id": "Frecuencia",
                    "valor": None
                }, {
                    "id": "PIP",
                    "valor": 369
                }, {
                    "id": "Corriente",
                    "valor": 139.3
                }]
            }, {
                "titulo": "VARIABLES SUPERFICIE",
                "contenido": [{
                    "id": "THP",
                    "valor": 200
                }, {
                    "id": "THT",
                    "valor": 369
                }]
            }, {
                "titulo": "CAUDALES",
                "contenido": [{
                    "id": "ACEITE BPD",
                    "valor": 200
                }, {
                    "id": "AGUA BPD",
                    "valor": 369
                }, {
                    "id": "FLUIDO BPD",
                    "valor": 369
                }, {
                    "id": "GAS MSFCD",
                    "valor": 369
                }]
            }, {
                "titulo": "PROPIEDADES",
                "contenido": [{
                    "id": "%S&W",
                    "valor": 200
                }, {
                    "id": "API @60ºF",
                    "valor": 369
                }, {
                    "id": "CLORUROS",
                    "valor": 369
                }, {
                    "id": "DILUYENTE",
                    "valor": 369
                }]
            }, {
                "titulo": "COMENTARIOS",
                "contenido": "MPFM1. BSW en seguimiento."
            }]
        }
        return dataPozoRepresentation
