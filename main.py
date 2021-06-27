import numpy as np
import time
import random

class Automaat:
    '''Een cellulaire automaat met rooster n
    een cel heeft m toestanden
    alle cellen in het rooster hebben dezelfde regels '''  
    
    '''Te doen: cellen maken, regels maken'''
    
    def __init__(self, dimensies, omvang, toestanden, randvoorwaarden,regelnummer):
        self.omvang = omvang
        self.rooster = Automaat.rooster(self,dimensies,omvang)
        self.toestanden = Automaat.toestanden(self,toestanden)
        self.regelnummer = regelnummer
    
    def rooster(self, dim, omvang): 
        '''maakt een rooster van lengte n in een gespecificeerde dimensie'''
        vorm = tuple(omvang for i in range(dim))
        #hier misschien nog een functie die de grid willekeurig vult met
        #nullen en enen, of om een input vraagt vanuit de user
        return np.zeros(vorm,dtype=int)
    
    def toestanden(self, toestanden): #toestand van een cel, m mogelijkheden
        return [i for i in range(toestanden)]
    

class eendimensionale_CA(Automaat):
    def regels(self,regelnummer):
        binair = [int(i) for i in format(regelnummer, 'b').zfill(8)]
        res = {"111": binair[0], "110": binair[1],
               "101": binair[2], "100": binair[3],
               "011": binair[4], "010": binair[5],
               "001": binair[6], "000": binair[7]}
        return res
    
    def randvoorwaarden(self):
        return 0
    
    def krijg_omgeving(self, i):
        res = str(self.rooster[i-1]) + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
        return res #periodiek
        
    def update_bord(self):
        nieuw_rooster = self.rooster
        regels = eendimensionale_CA.regels(self,self.regelnummer)
        for i in range(self.omvang):
            omgeving = eendimensionale_CA.krijg_omgeving(self,i)
            print(omgeving)
            nieuw_rooster[i] = regels[omgeving]
        self.rooster = nieuw_rooster

#Eendimensionaal test
a_30 = eendimensionale_CA(1,10,2,0,30)
a_30.rooster[4:7] = [1,0,1]
while True:
    a_30.update_bord()
    print(a_30.rooster)
    time.sleep(0.5)
    break


class tweedimensionale_CA(Automaat):
    def regels(self,regelnummer):
        binair = [int(i) for i in format(regelnummer, 'b').zfill(512)]
        #Een functie die voor i in range(512) string aanmaakt met binair[i]
        res = {}
        for i in reversed(range(512)):
            res[format(i, 'b').zfill(9)] = binair[i]
        return res
    
    def randvoorwaarden(self):
        return 0
    
    def krijg_omgeving(self, r, c):
        res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)%len(self.rooster)])
        res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)%len(self.rooster)])
        res3 = str(self.rooster[(r+1)%len(self.rooster)][c-1]) + str(self.rooster[(r+1)%len(self.rooster)][c]) + str(self.rooster[(r+1)%len(self.rooster)][(c+1)%len(self.rooster)])
        return res1 + res2 + res3 #periodiek
        
    def update_bord(self):
        nieuw_rooster = self.rooster
        regels = tweedimensionale_CA.regels(self,self.regelnummer) #regels moeten eigenlijk in de init al gedaan worden
        for rij in range(self.omvang):
            for kolom in range(self.omvang):
                omgeving = tweedimensionale_CA.krijg_omgeving(self,rij,kolom)
                nieuw_rooster[rij][kolom] = regels[omgeving]
        self.rooster = nieuw_rooster
        return self.rooster
    
    def __str__(self): #kan nog wat mooier
        res = ''
        for rij in range(self.omvang):
            res += ''.join(map(str,self.rooster[rij])) + '\n'
        return res


#%%Tweedimensionale test
a_100 = tweedimensionale_CA(2,10,2,0,47634829485252037513200973884082471888288955642325528262910887637847274372981720534370017768342996036219492316860704401273651054628223608960)
a_100.rooster = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
print(a_100.rooster)
while True:
    a_100.update_bord()
    print(a_100)
    time.sleep(0.5)

    

