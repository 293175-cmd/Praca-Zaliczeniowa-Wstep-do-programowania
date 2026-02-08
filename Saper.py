import random

def gen_plansza(x,y,z,stX,stY):
    mapa=[[0 for _ in range(x)] for _ in range(y)]
    mapa[stX][stY]='O'
    for i in range(z): #Generowanie min (miny oznaczone 'X')
        minaX=random.randint(0,9)
        minaY=random.randint(0,9)
        while (mapa[minaX][minaY]=='X' or ((abs(stX - minaX) <= 1) and (abs(stY - minaY) <=1))):
            minaX=random.randint(0,9)
            minaY=random.randint(0,9)
        mapa[minaX][minaY]='X'

    for i in range(x): #Przypisywanie wartosci pol 
        for j in range(y):
            licznik=0
            if (mapa[i][j] !='O' and mapa[i][j] != "X"):
                for k in range(-1,2):
                    for l in range(-1,2):
                        if ((i+k>=0) and (j+l>=0)):
                            if ((i+k<=x-1) and (j+l<=y-1)):
                                if (mapa[i+k][j+l]=='X'):
                                    licznik=licznik+1
                mapa[i][j]=licznik

    return mapa
    pass

strzalx=5
strzaly=7
szerokosc=10 #X
wysokosc=10 #Y
miny=15
plansza=gen_plansza(szerokosc,wysokosc,miny,strzalx,strzaly)
for i in range(wysokosc):
    print(plansza[i])
