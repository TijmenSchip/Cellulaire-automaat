'''regelnummer uitrekenen game of life''' 
omgevingen = []
for i in range(512):
    omgevingen.append([int(j) for j in format(i, 'b').zfill(9)])
    
regelset = {}
for i in omgevingen:
    stringvorm = ''
    for j in i:
        stringvorm+=str(j)
    som = sum(i[:4]) + sum(i[5:])
    if i[4] == 0:
        if som == 3: 
            regelset[stringvorm] = 1
        else:
            regelset[stringvorm] = 0
    if i[4] == 1:
        if som < 2:
            regelset[stringvorm] = 0
        elif som == 2 or som == 3:
            regelset[stringvorm] = 1
        elif som > 3:
            regelset[stringvorm] = 0

regelnummer = 0
for i in range(512):
    binair = format(i, 'b').zfill(9)
    if regelset[binair] == 1:
        regelnummer+=2**(i-1)

