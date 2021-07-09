
import math


class Calculos():
    def __init__(self):
        # self.aceite = kargs["aceite"]
        # self.swCabeza = kargs["swCabeza"]
        # self.geCabeza = kargs["geCabeza"]
        # self.geEmulsion = kargs["geEmulsion"]
        # self.apiCabeza = kargs["apiCabeza"]
        # self.apiDiluyente = kargs["apiDiluyente"]
        self.densidadAgua = 62.3774

        self.apiAgua = 10
        self.viscosidadAgua = 1.15

        #              tabla5   |   tabla6
        self.refutaA = 14.534  # 68313767.0487542
        self.refutaB = 0.8  # 0.736
        self.refutaC = 10.975  # -868912303.413984
        self.chevron2A = 1000  # 248.0055810
        self.chevron2B = 1  # 1
        self.chevron2C = 1  # 1
        self.parkashA = 376.38  # 57.00322402
        self.parkashB = 0.93425  # 0.734
        self.parkashC = 157.43  # 683.72032059

    def setVariables(self, **kargs):
        for k in kargs.keys():
            self.__setattr__(k, kargs[k])

    def calcularDiluyente(self, decApiCabeza, decApiDiluyente, decApiMezclaDeseado, decAceite, decSwCabeza, condicion):
        apiCabeza = float(decApiCabeza)
        apiDiluyente = float(decApiDiluyente)
        apiMezclaDeseado = float(decApiMezclaDeseado)
        aceite = float(decAceite)
        swCabeza = float(decSwCabeza)/100
        apiMezclaObjetivo = apiMezclaDeseado
        geAceite = 141.5 / (apiCabeza + 131.5)
        geAgua = 1
        geDiluyente = 141.5 / (apiDiluyente + 131.5)

        agua = (aceite * swCabeza) / (1 - swCabeza)
        ejecucion = True
        if apiMezclaDeseado < apiDiluyente:
            while ejecucion:
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
                    ejecucion = False
                if not condicion:
                    ejecucion = condicion
            self.calcularViscosidad(apiCabeza, apiDiluyente,
                                    apiMezclaHumedo, aceite, agua, diluyente)
            self.setVariables(geMezclaSeco=geMezclaSeco, geDiluyente=geDiluyente, geAceite=geAceite, geLiquido=geLiquido,
                              agua=agua, swMezcla=swMezcla, diluyente=diluyente, aceite=aceite,  factorEncogimiento=factorS,
                              apiMezclaHumedo=apiMezclaHumedo, apiMezclaSeco=apiMezclaSeco,
                              densidadEmulsion=self.densidadAgua*geMezclaSeco, densidadDiluyente=self.densidadAgua*geDiluyente, densidadLiquido=self.densidadAgua*geLiquido,
                              relacionOil_Diluyente=diluyente /
                              (aceite+diluyente),
                              relacion1_3=aceite/3)
        else:
            self.setVariables(
                status="el valor de API supera al del diluyente")

    def calcularAPI(self, decApiCabeza, decApiDiluyente, decDiluyente, decAceite, decSwCabeza):
        apiCabeza = float(decApiCabeza)
        apiDiluyente = float(decApiDiluyente)
        diluyente = float(decDiluyente)
        aceite = float(decAceite)
        swCabeza = float(decSwCabeza)/100

        geAceite = 141.5 / (apiCabeza + 131.5)
        geAgua = 1
        geDiluyente = 141.5 / (apiDiluyente + 131.5)

        agua = (aceite * swCabeza) / (1 - swCabeza)

        factorC = (diluyente / (diluyente + aceite)) * 100
        factorG = apiDiluyente - apiCabeza
        factorS = 4.86 * pow(10, -8) * factorC * \
            pow(100 - factorC, 0.819) * pow(factorG, 2.28)
        # factorS=2.14*pow(10, -3)*pow(factorC,-0.0704)*pow(factorG,1.76)
        encogimiento = (factorS / 100) * (diluyente + aceite)

        geMezclaHumedo = (aceite * geAceite + agua * geAgua + diluyente *
                          geDiluyente) / (aceite + agua + diluyente - encogimiento)
        geMezclaSeco = (aceite * geAceite + diluyente *
                        geDiluyente) / (aceite + diluyente - encogimiento)
        # geMezcla = (aceite * geAceite + agua * geAgua + diluyente * geDiluyente) / (aceite + agua + diluyente)# SIN ENCOGIMIENTO

        swMezcla = agua / (agua + diluyente + aceite)

        apiMezclaHumedo = (141.5 / geMezclaHumedo) - 131.5
        apiMezclaSeco = (141.5 / geMezclaSeco) - 131.5

        geLiquido = 141.5 / (131.5 + apiMezclaHumedo)

        self.calcularViscosidad(apiCabeza, apiDiluyente,
                                apiMezclaHumedo, aceite, agua, diluyente)

        self.setVariables(geMezclaSeco=geMezclaSeco, geDiluyente=geDiluyente, geAceite=geAceite, geLiquido=geLiquido,
                          agua=agua, swMezcla=swMezcla, diluyente=diluyente, aceite=aceite,  factorEncogimiento=factorS,
                          apiMezclaHumedo=apiMezclaHumedo, apiMezclaSeco=apiMezclaSeco,
                          densidadEmulsion=self.densidadAgua*geMezclaSeco, densidadDiluyente=self.densidadAgua*geDiluyente, densidadLiquido=self.densidadAgua*geLiquido,
                          relacionOil_Diluyente=diluyente/(aceite+diluyente),
                          relacion1_3=aceite/3)

    def calcularLaboratorio(self, decApiMezcla, decSwMezcla):
        swMezcla = float(decSwMezcla)
        apiMezcla = float(decApiMezcla)

        geMezclaSeco = 141.5/(131.5+apiMezcla)
        densidadEmulsion = geMezclaSeco*self.densidadAgua
        densidadLiquido = (1-(swMezcla/100))*densidadEmulsion + \
            (swMezcla/100)*self.densidadAgua
        geLiquido = densidadLiquido/self.densidadAgua
        apiLiquido = (141.5/geLiquido)-131.5

        self.setVariables(geMezclaSeco=geMezclaSeco, geLiquido=geLiquido,
                          apiMezclaHumedo=apiLiquido, apiMezclaSeco=apiMezcla,
                          densidadEmulsion=densidadEmulsion, densidadLiquido=densidadLiquido, densidaAgua=self.densidadAgua)

    def calcularViscosidad(self, apiCabeza, apiDiluyente, apiMezclaHumedo, vAceite, vAgua, vDiluyente):
        viscosidadCinematicaCrudo = 55332503.7292 * math.exp(-0.6474*apiCabeza)
        viscosidadCinematicaDiluyente = 4585.7*pow(apiDiluyente, -2.165)
        irc = self.refutaA * \
            math.log(math.log(viscosidadCinematicaCrudo +
                     self.refutaB))+self.refutaC
        ird = self.refutaA * \
            math.log(math.log(viscosidadCinematicaDiluyente +
                     self.refutaB))+self.refutaC
        irw = self.refutaA * \
            math.log(math.log(self.viscosidadAgua +
                     self.refutaB))+self.refutaC
        vTotal = vAceite+vAgua+vDiluyente
        xmic = ((131.5+apiMezclaHumedo)/(131.5+apiCabeza))*(vAceite/vTotal)
        xmid = ((131.5+apiMezclaHumedo)/(131.5+apiDiluyente)) * \
            (vDiluyente/vTotal)
        xmiw = ((131.5+apiMezclaHumedo)/(131.5+self.apiAgua))*(vAgua/vTotal)
        xmiTotal = xmiw+xmic+xmid
        indiceRefutac = irc*xmic
        indiceRefutad = ird*xmid
        indiceRefutaw = irw*xmiw
        indiceRefutaMezcla = indiceRefutac+indiceRefutad+indiceRefutaw

        viscocidadCinematicaMezcla = pow(pow(math.exp(1), math.exp(
            1)), (indiceRefutaMezcla-self.refutaC)/self.refutaA)-self.refutaB

        self.setVariables(viscosidadMezcla=viscocidadCinematicaMezcla,
                          viscosidadAceite=viscosidadCinematicaCrudo,
                          viscosidadDiluyente=viscosidadCinematicaDiluyente)
