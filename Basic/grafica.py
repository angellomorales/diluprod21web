

class Grafica():

    def __init__(self, **kwargs):
        self.addParameters(**kwargs)
        self.seriesParams = {}
        self.dataGraph = []

    def getGraphParams(self):
        return self.__dict__

    def addParameters(self, **kwargs):
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def addSerieParameters(self, **kwargs):
        if(kwargs['serie'] in self.seriesParams):
            serie = self.seriesParams[kwargs['serie']]
        else:
            serie = {}
        for k in kwargs.keys():
            if k != 'serie':
                serie[k] = kwargs[k]

        self.seriesParams[kwargs['serie']] = serie

    def addSeriesData(self, **kwargs):
        data = {}
        for k in kwargs.keys():
            data[k] = kwargs[k]

        self.dataGraph.append(data)
