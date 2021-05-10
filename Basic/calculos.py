class NewCalculos():
    def __init__(self, **kargs):
        # self.aceite = aceite
        # self.swCabeza = swCabeza
        # self.apiCabeza = apiCabeza
        # self.apiDiluyente = apiDiluyente
        self.densidadAgua = 62.3774

    def calcularDiluyente(apiCabeza, apiDiluyente, apiMezclaDeseado, aceite, swCabeza, condicion)
       apiMezclaObjetivo = apiMezclaDeseado
        geAceite = 141.5 / (apiCabeza + 131.5)
        geAgua = 1
        geDiluyente = 141.5 / (apiDiluyente + 131.5)

        agua = (aceite * swCabeza) / (1 - swCabeza)

        while condicion
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

            gemyLiquido = 141.5 / (131.5 + apiMezclaHumedo)

            # --------condicional de acercamiento de api---------
            res = round(apiMezclaSeco, 2) - round(apiMezclaDeseado, 2)
            if (res > 0)
               if (res > 2)
                   apiMezclaObjetivo = apiMezclaObjetivo - 1
                else
                   apiMezclaObjetivo = apiMezclaObjetivo - 0.01
            else
               apiMezclaObjetivo = apiMezclaObjetivo + 0.01
            if ((res < 0.01 and res > -0.01) or (res < 0.5 and res > -0.5 and swCabeza > 0.9) or (res < 0.1 and res > -0.1 and swCabeza > 0.7))
               condicion = false
        setVariables(geMezclaSeco, geDiluyente, agua, swMezcla, diluyente, aceite,
                     geAceite, factorS, apiMezclaHumedo, apiMezclaSeco, gemyLiquido)

    def setVariables(self, **kargs):        
        self.agua = agua
        self.diluyente = diluyente

        self.swMezcla = swMezcla

        self.apiMezclaHumedo = apiMezclaHumedo
        self.apiMezclaSeco = apiMezclaSeco

        self.geCabeza = geCabeza
        self.geDiluyente = geDiluyente
        self.geEmulsion = geEmulsion
        self.geLiquido = geLiquido
      
        self.densidadEmulsion = self.densidadAgua*self.geMezclaSeco
        self.densidadDiluyente = self.densidadAgua*self.geDiluyente
        self.densidadLiquido = self.densidadAgua*self.geLiquido

        self.relacionOil_Diluyente = diluyente/(aceite+diluyente)
        self.relacion1_3 = relacion1_3=aceite/3

        self.factorEncogimiento = factorEncogimiento
