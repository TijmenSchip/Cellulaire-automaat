import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

class Automaat:
    '''Een cellulaire automaat met rooster n
    een cel heeft m toestanden
    alle cellen in het rooster hebben dezelfde regels '''  

    '''Te doen: cellen maken, regels maken'''

    def __init__(self, dimensies, omvang, toestanden, randvoorwaarden):
        self.rooster = Automaat.rooster(self,dimensies,omvang)
        self.toestanden = Automaat.toestanden(self,toestanden)
        self.randvoorwaarden = Automaat.randvoorwaarden(self,randvoorwaarden)

    def rooster(self, dim, omvang): 
        '''maakt een rooster van lengte n in een gespecificeerde dimensie'''
        vorm = tuple(omvang for i in range(dim))
        return np.zeros(vorm, dtype = int)

    def toestanden(self, m): #toestand van een cel, m mogelijkheden
        return [i for i in range(m)]

    def randvoorwaarden(self,randvoorwaarde):
        if randvoorwaarde == "periodiek":
            '''rechterbuur van laatste cel is eerste cel en linkerbuurt eerste is laatste'''
            return 0
        return 0
