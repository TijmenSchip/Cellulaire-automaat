'''regelnummer uitrekenen Game of Life''' 
omgevingen = []
for i in range(512):
    omgevingen.append([int(j) for j in format(i, 'b').zfill(9)])
    
regelset = {} #dit wordt de regelset voor The Game of Life
for i in omgevingen:
    stringvorm = '' #zet de omgeving om van lijst naar string
    for j in i:
        stringvorm+=str(j)
    som = sum(i[:4]) + sum(i[5:]) #aantal (andere) levende cellen in de omgeving
    if i[4] == 0: #de middelste cel leeft niet
        if som == 3: 
            regelset[stringvorm] = 1
        else:
            regelset[stringvorm] = 0
    if i[4] == 1: #de middelste cel leeft wel
        if som < 2:
            regelset[stringvorm] = 0
        elif som == 2 or som == 3:
            regelset[stringvorm] = 1
        elif som > 3:
            regelset[stringvorm] = 0

regelnummer = 0 #zet de dictionary voor de regels om in een getal
for i in range(512):
    binair = format(i, 'b').zfill(9)
    if regelset[binair] == 1:
        regelnummer+=2**(511-i)
