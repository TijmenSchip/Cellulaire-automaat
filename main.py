import numpy as np
import pygame, random, sys, time

class Automaat:
    '''Een cellulaire automaat met rooster n
    een cel heeft m toestanden
    alle cellen in het rooster hebben dezelfde regels '''  
    
    '''Te doen: cellen maken, regels maken'''
    
    def __init__(self, dimensies, omvang, toestanden, randvoorwaarde, regelnummer):
        self.omvang = omvang
        self.rooster = Automaat.rooster(self,dimensies,omvang)
        self.toestanden = Automaat.toestanden(self,toestanden)
        self.regelnummer = regelnummer
        self.randvoorwaarde = randvoorwaarde
    
    def rooster(self, dimensies, omvang): 
        '''maakt een rooster van lengte n in een gespecificeerde dimensie'''
        vorm = tuple(omvang for i in range(dimensies))
        #hier misschien nog een functie die de grid willekeurig vult met
        #nullen en enen, of om een input vraagt vanuit de user
        return np.zeros(vorm,dtype=int)
    
    def toestanden(self, toestanden): #toestand van een cel, m mogelijkheden
        return [i for i in range(toestanden)]
    
class eendimensionale_CA(Automaat):
    def __init__(self, dimensies, omvang, toestanden, randvoorwaarden, regelnummer):
        super().__init__(dimensies, omvang, toestanden, randvoorwaarden, regelnummer)
        self.regels = eendimensionale_CA.regels(self,self.regelnummer)
    
    def regels(self,regelnummer):
        binair = [int(i) for i in format(regelnummer, 'b').zfill(8)]
        res = {"111": binair[0], "110": binair[1],
               "101": binair[2], "100": binair[3],
               "011": binair[4], "010": binair[5],
               "001": binair[6], "000": binair[7]}
        return res
    
    def krijg_omgeving(self, i):
        if self.randvoorwaarde == 'periodiek':
            res = str(self.rooster[i-1]) + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
        if self.randvoorwaarde == 'Dirichlet0':
            if i == 0:
                res = '0' + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
            elif i == self.omvang - 1:
                res = str(self.rooster[i-1]) + str(self.rooster[i]) + '0'
            else:
                res = str(self.rooster[i-1]) + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
        if self.randvoorwaarde == 'Dirichlet1':
            if i == 0:
                res = '1' + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
            elif i == self.omvang - 1:
                res = str(self.rooster[i-1]) + str(self.rooster[i]) + '1'
            else:
                res = str(self.rooster[i-1]) + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
        if self.randvoorwaarde == 'Neumann':
            if i == 0:
                res = str(self.rooster[i]) + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
            elif i == self.omvang - 1:
                res = str(self.rooster[i-1]) + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
            else:
                res = str(self.rooster[i-1]) + str(self.rooster[i]) + str(self.rooster[(i+1)%self.omvang])
        return res #periodiek
        
    def update_bord(self):
        nieuw_rooster = [0 for i in range(self.omvang)]
        for i in range(self.omvang):
            omgeving = eendimensionale_CA.krijg_omgeving(self,i)
            nieuw_rooster[i] = self.regels[omgeving]
        self.rooster = nieuw_rooster

    def random_rooster(self):
        #initialiseert een random rooster gevuld met integers 0 en 1
        rooster = []
        for cel in range(self.omvang):
            rooster.append(random.randint(0,1))
        self.rooster = rooster
        
    def visualisatie_cel(x_positie, y_positie, kleur_levende_cel, cel_breedte, cel_hoogte):
        #tekent een cel op (x_positie, y_positie) in het scherm met kleur kleur_levende_cel
        x_positie *= cel_breedte
        y_positie *= cel_hoogte
        pygame.draw.ellipse(scherm, kleur_levende_cel, (x_positie, y_positie, cel_breedte, cel_hoogte))

    def visualisatie_bord(self, breedte_scherm, hoogte_scherm, disco = False):
        #gebruikt pygame om een eendimensionaal CA te visualiseren
        scherm_settings(breedte_scherm, hoogte_scherm)
        kleur_levende_cel = pygame.Color(200,0,0)
        kleur_dode_cel = (0,0,0)
        cel_breedte = breedte_scherm // self.omvang
        cel_hoogte = hoogte_scherm // self.omvang
        kleursprong = 0
        
        eendimensionale_CA.random_rooster(self)
        
        while True:
            #tekent alle cellen op het scherm
            for rij in range(hoogte_scherm // cel_hoogte):
                # Sluit scherm als gebruiker op kruisje klikt
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                #tekent alle cellen in een rij
                for cel_index in range(self.omvang):
                    cel_waarde = self.rooster[cel_index]
                    if cel_waarde == 1:
                        cel_kleur = kleur_levende_cel
                    else:
                        cel_kleur = kleur_dode_cel
                    eendimensionale_CA.visualisatie_cel(cel_index, rij, cel_kleur, cel_breedte, cel_hoogte)
                
                #geeft de mogelijkheid om de kleuren van de levende cellen periodiek te veranderen
                if disco == True:
                    kleursprong = (kleursprong + 10) % 360
                    kleur_levende_cel.hsva = [kleursprong, 100, 100]
                
                #update scherm en rooster
                pygame.display.flip()
                eendimensionale_CA.update_bord(self)
                
                time.sleep(1)
            
class tweedimensionale_CA(Automaat):
    def __init__(self, dimensies, omvang, toestanden, randvoorwaarden,regelnummer):
        super().__init__(dimensies, omvang, toestanden, randvoorwaarden,regelnummer)
        self.regels = tweedimensionale_CA.regels(self,self.regelnummer)
        
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
        if self.randvoorwaarde == 'periodiek':
            res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)%self.omvang])
            res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)%self.omvang])
            res3 = str(self.rooster[(r+1)%self.omvang][c-1]) + str(self.rooster[(r+1)%self.omvang][c]) + str(self.rooster[(r+1)%self.omvang][(c+1)%self.omvang])
        if self.randvoorwaarde == 'Dirichlet0':
            if r == 0:
                if c == 0:
                    res1 = '000'
                    res2 = '0' + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = '0' + str(self.rooster[(r+1)][c]) + str(self.rooster[(r+1)][(c+1)])
                elif c == self.omvang - 1:
                    res1 = '000'
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + '0'
                    res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + '0'
                else:
                    res1 = '000'
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + str(self.rooster[(r+1)][(c+1)])
            elif r == self.omvang - 1:
                if c == 0:
                    res1 =  '0' + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                    res2 = '0' + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = '000'
                elif c == self.omvang -1:
                    res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + '0'
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + '0'
                    res3 = '000'
                else:
                    res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = '000'
            elif c == 0:
                res1 = '0' + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                res2 = '0' + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                res3 = '0' + str(self.rooster[(r+1)%self.omvang][c]) + str(self.rooster[(r+1)][(c+1)])
            elif c == self.omvang - 1:
                res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + '0'
                res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + '0'
                res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + '0'
            else:
                res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + str(self.rooster[(r+1)][(c+1)])
        if self.randvoorwaarde == 'Dirichlet1':
            if r == 0:
                if c == 0:
                    res1 = '111'
                    res2 = '1' + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = '1' + str(self.rooster[(r+1)][c]) + str(self.rooster[(r+1)][(c+1)])
                elif c == self.omvang - 1:
                    res1 = '111'
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + '1'
                    res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + '1'
                else:
                    res1 = '111'
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + str(self.rooster[(r+1)][(c+1)])
            elif r == self.omvang - 1:
                if c == 0:
                    res1 = '1' + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                    res2 = '1' + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = '111'
                elif c == self.omvang -1:
                    res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + '1'
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + '1'
                    res3 = '111'
                else:
                    res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                    res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                    res3 = '111'
            elif c == 0:
                res1 = '1' + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                res2 = '1' + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                res3 = '1' + str(self.rooster[(r+1)%self.omvang][c]) + str(self.rooster[(r+1)][(c+1)])
            elif c == self.omvang - 1:
                res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + '1'
                res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + '1'
                res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + '1'
            else:
                res1 = str(self.rooster[r-1][c-1]) + str(self.rooster[r-1][c]) + str(self.rooster[r-1][(c+1)])
                res2 = str(self.rooster[r][c-1]) + str(self.rooster[r][c]) + str(self.rooster[r][(c+1)])
                res3 = str(self.rooster[(r+1)][c-1]) + str(self.rooster[(r+1)][c]) + str(self.rooster[(r+1)][(c+1)])
        return res1 + res2 + res3 
        
    def update_bord(self):
        nieuw_rooster = []
        for i in range(self.omvang):
            nieuw_rooster.append([0 for j in range(self.omvang)])
        for rij in range(self.omvang):
            for kolom in range(self.omvang):
                omgeving = tweedimensionale_CA.krijg_omgeving(self,rij,kolom)
                nieuw_rooster[rij][kolom] = self.regels[omgeving]
        self.rooster = nieuw_rooster
    
    def random_rooster(self):
        #initialiseert een random rooster van lengte omvang en breedte omvang gevuld met integers 0 en 1
        rooster = []
        for rij in range(self.omvang):
            lijst = []
            for kolom in range(self.omvang):
                lijst.append(random.randint(0,1))
            rooster.append(lijst)
        self.rooster = rooster
    
    def __str__(self): #kan nog wat mooier
        res = ''
        for rij in range(self.omvang):
            res += ''.join(map(str,self.rooster[rij])) + '\n'
        return res
    
    def visualisatie_cel(x_positie, y_positie, kleur_levende_cel, cel_breedte, cel_hoogte):
        #tekent een cel op (x_positie, y_positie) in het scherm met kleur kleur_levende_cel
        x_positie *= cel_breedte
        y_positie *= cel_hoogte
        pygame.draw.ellipse(scherm, kleur_levende_cel, (x_positie, y_positie, cel_breedte, cel_hoogte))
    
    def visualisatie_bord(self, breedte_scherm, hoogte_scherm, disco = False):
        #gebruikt pygame om een tweedimensionaal CA te visualiseren
        scherm_settings(breedte_scherm, hoogte_scherm)
        kleur_levende_cel = pygame.Color(200,0,0)
        kleur_dode_cel = (0,0,0)
        cel_breedte = breedte_scherm // self.omvang
        cel_hoogte = hoogte_scherm // self.omvang
        kleursprong = 0
        
        tweedimensionale_CA.random_rooster(self)
        
        while True:
            # Sluit scherm als gebruiker op kruisje klikt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            #tekent alle cellen op het scherm
            for rij in range(self.omvang):
                for kolom in range(self.omvang):
                    cel_waarde = self.rooster[rij][kolom]
                    if cel_waarde == 1:
                        cel_kleur = kleur_levende_cel
                    else:
                        cel_kleur = kleur_dode_cel
                    tweedimensionale_CA.visualisatie_cel(rij, kolom, cel_kleur, cel_breedte, cel_hoogte)
            
            #geeft de mogelijkheid om de kleuren van de levende cellen periodiek te veranderen
            if disco == True:
                kleursprong = (kleursprong + 2) % 360
                kleur_levende_cel.hsva = [kleursprong, 100, 100]
                
            #update scherm en rooster
            pygame.display.flip()
            tweedimensionale_CA.update_bord(self)
            time.sleep(0.1)
                         
def scherm_settings(breedte_scherm, hoogte_scherm):
    #initialiseert pygame scherm
    #parameters van scherm zijn: ((breedte, hoogte), type scherm, aantal bits voor kleuren)
    global scherm
    scherm = pygame.display.set_mode((breedte_scherm, hoogte_scherm), 0, 24) 

def main():
    #hoofdfunctie waarin het programma aangestuurd kan worden
    regelnummer_gameoflife = 56893936281229891685721266345642969019123084627443426808421779969651967409186101770533392600047921391326336606991482847057223097055804786096169470132224

    gol = tweedimensionale_CA(2,50,2,'Dirichlet1',regelnummer_gameoflife)
    tweedimensionale_CA.visualisatie_bord(gol, 600, 600, True)
    
    r30 = eendimensionale_CA(1, 15, 2, 'periodiek', 30)
    eendimensionale_CA.visualisatie_bord(r30, 400, 400, True)
    
if __name__ == '__main__':
    main()
