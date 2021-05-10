class NewCalculos():
    def calcularDiluyente(apiCabeza, apiNafta, apiMezclaDeseado, aceite, swCabeza, condicion)
      apiMezclaObjetivo = apiMezclaDeseado
       geAceite = 141.5 / (apiCabeza + 131.5)
        geAgua = 1
        geNafta = 141.5 / (apiNafta + 131.5)

        agua = (aceite * swCabeza) / (1 - swCabeza)

        while condicion
          geMezclaSeco = 141.5 / (apiMezclaObjetivo + 131.5)
           nafta = (aceite * (geAceite - geMezclaSeco) + agua *
                    (geAgua - geMezclaSeco)) / (geMezclaSeco - geNafta)

            factorC = (nafta / (nafta + aceite)) * 100
            factorG = apiNafta - apiCabeza
            factorS = 4.86 * pow(10, -8) * factorC * \
                                 pow(100 - factorC, 0.819) * pow(factorG, 2.28)
            # factorS=2.14*Math.pow(10, -3)*pow(factorC,-0.0704)*pow(factorG,1.76)
            encogimiento = (factorS / 100) * (nafta + aceite)

            geMezclaHumedo = (aceite * geAceite + agua * geAgua +
                              nafta * geNafta) / (aceite + agua + nafta - encogimiento)
            geMezclaSeco = (aceite * geAceite + nafta * geNafta) / \
                            (aceite + nafta - encogimiento)

            swMezcla = agua / (agua + nafta + aceite - encogimiento)
            # nafta = (aceite * (geAceite - geMezclaSeco) + agua * (geAgua - geMezclaSeco)) / (geMezclaSeco - geNafta)

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
