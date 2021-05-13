class NewCalculos():
    def __init__(self):
        # self.aceite = kargs["aceite"]
        # self.swCabeza = kargs["swCabeza"]
        # self.geCabeza = kargs["geCabeza"]
        # self.geEmulsion = kargs["geEmulsion"]
        # self.apiCabeza = kargs["apiCabeza"]
        # self.apiDiluyente = kargs["apiDiluyente"]
        self.densidadAgua = 62.3774

    def setVariables(self, **kargs):
        for k in kargs.keys():
            self.__setattr__(k, kargs[k])

    def calcularDiluyente(self, decApiCabeza, decApiDiluyente, decApiMezclaDeseado, decAceite, decSwCabeza, condicion):
        apiCabeza = float(decApiCabeza)
        apiDiluyente = float(decApiDiluyente)
        apiMezclaDeseado = float(decApiMezclaDeseado)
        aceite = float(decAceite)
        swCabeza = float(decSwCabeza)
        apiMezclaObjetivo = apiMezclaDeseado
        geAceite = 141.5 / (apiCabeza + 131.5)
        geAgua = 1
        geDiluyente = 141.5 / (apiDiluyente + 131.5)

        agua = (aceite * swCabeza) / (1 - swCabeza)

        while condicion:
            geMezclaSeco = 141.5 / (apiMezclaObjetivo + 131.5)
            diluyente = (aceite * (geAceite - geMezclaSeco) + agua *
                         (geAgua - geMezclaSeco)) / (geMezclaSeco - geDiluyente)

            factorC = (diluyente / (diluyente + aceite)) * 100
            factorG = apiDiluyente - apiCabeza
            factorS = 4.86 * pow(10, -8) * factorC * \
                pow(100 - factorC, 0.819) * pow(factorG, 2.28)
            # factorS=2.14*Math.pow(10, -3)*pow(factorC,-0.0704)*pow(factorG,1.76)
            encogimiento = (factorS / 100) * (diluyente + aceite)

            geMezclaHumedo = (aceite * geAceite + agua * geAgua +
                              diluyente * geDiluyente) / (aceite + agua + diluyente - encogimiento)
            geMezclaSeco = (aceite * geAceite + diluyente * geDiluyente) / \
                (aceite + diluyente - encogimiento)

            swMezcla = agua / (agua + diluyente + aceite - encogimiento)
            # diluyente = (aceite * (geAceite - geMezclaSeco) + agua * (geAgua - geMezclaSeco)) / (geMezclaSeco - geDiluyente)

            apiMezclaHumedo = (141.5 / geMezclaHumedo) - 131.5
            apiMezclaSeco = (141.5 / geMezclaSeco) - 131.5

            geLiquido = 141.5 / (131.5 + apiMezclaHumedo)

            # --------condicional de acercamiento de api---------
            res = round(apiMezclaSeco, 2) - round(apiMezclaDeseado, 2)
            if (res > 0):
                if (res > 2):
                    apiMezclaObjetivo = apiMezclaObjetivo - 1
                else:
                    apiMezclaObjetivo = apiMezclaObjetivo - 0.01
            else:
                apiMezclaObjetivo = apiMezclaObjetivo + 0.01
            if ((res < 0.01 and res > -0.01) or (res < 0.5 and res > -0.5 and swCabeza > 0.9) or (res < 0.1 and res > -0.1 and swCabeza > 0.7)):
                condicion = False
        self.setVariables(geMezclaSeco=geMezclaSeco, geDiluyente=geDiluyente, geAceite=geAceite, geLiquido=geLiquido,
                           agua=agua, swMezcla=swMezcla, diluyente=diluyente, aceite=aceite,  factorEncogimiento=factorS,
                           apiMezclaHumedo=apiMezclaHumedo, apiMezclaSeco=apiMezclaSeco,
                           relacionOil_Diluyente=diluyente/(aceite+diluyente),
                           relacion1_3=aceite/3)
