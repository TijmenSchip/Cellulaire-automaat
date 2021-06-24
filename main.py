import numpy as np

class Automaat:
    '''Een cellulaire automaat met rooster n
    een cel heeft m toestanden
    alle cellen in het rooster hebben dezelfde regels '''  
    
    '''Te doen: cellen maken, regels maken'''
    
    def __init__(self, dimensies, omvang, toestanden, randvoorwaarden,regelnummer=0):
        self.rooster = Automaat.rooster(self,dimensies,omvang)
        self.toestanden = Automaat.toestanden(self,toestanden)
        self.randvoorwaarden = Automaat.randvoorwaarden(self,randvoorwaarden)
    
    def rooster(self, dim, omvang): 
        '''maakt een rooster van lengte n in een gespecificeerde dimensie'''
        vorm = tuple(omvang for i in range(dim))
        return np.zeros(vorm,dtype=int)
    
    def toestanden(self, m): #toestand van een cel, m mogelijkheden
        return [i for i in range(m)]
    
    def randvoorwaarden(self,randvoorwaarde):
        if randvoorwaarde == "periodiek":
            '''rechterbuur van laatste cel is eerste cel en linkerbuurt eerste is laatste'''
            return 0
        return 0

class eendimensionale_CA(Automaat):
    def regels(self):
        binair = [int(i) for i in format(self.regelnummer, 'b').zfill(8)]
        res = {"111": binair[0], "110": binair[1],
               "101": binair[2], "100": binair[3],
               "011": binair[4], "010": binair[5],
               "001": binair[6], "000": binair[7]}
        return res
