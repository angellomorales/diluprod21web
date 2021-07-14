

class Grafica():

    def __init__(self, **kwargs):
        self.addParameters(**kwargs)
        self.seriesParams = {}

    def getGraphParams(self):
        return self.__dict__

    def addParameters(self, **kwargs):
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def addSerieParameters(self, **kwargs):
        serie = {}
        for k in kwargs.keys():
            if k != 'serie':
                serie[k] = kwargs[k]
        serie['pointRadius'] = 3
        serie['pointBorderColor'] = 'rgb(125, 125, 125)'

        self.seriesParams[kwargs['serie']]=serie
