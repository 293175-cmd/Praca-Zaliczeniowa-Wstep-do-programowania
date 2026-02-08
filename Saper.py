import random

def gen_plansza(x,y,z,stX,stY):
    mapa=[[0 for _ in range(x)] for _ in range(y)]
    mapa[stY][stX]='O'
    for i in range(z): #Generowanie min (miny oznaczone 'X')
        minaX=random.randint(0,x-1)
        minaY=random.randint(0,y-1)
        while (mapa[minaY][minaX]=='X' or ((abs(stX - minaX) <= 1) and (abs(stY - minaY) <=1))):
            minaX=random.randint(0,x-1)
            minaY=random.randint(0,y-1)
        mapa[minaY][minaX]='X'

    for i in range(y): #Przypisywanie wartosci pol 
        for j in range(x):
            licznik=0
            if (mapa[i][j] !='O' and mapa[i][j] != "X"):
                for k in range(-1,2):
                    for l in range(-1,2):
                        if ((i+k>=0) and (j+l>=0)):
                            if ((i+k<=y-1) and (j+l<=x-1)):
                                if (mapa[i+k][j+l]=='X'):
                                    licznik=licznik+1
                mapa[i][j]=licznik

    return mapa
    pass
def war_cal(x): #Sprawdzenie czy podana liczba jest calkowita
    try:
        int(x)
        return True
    except (ValueError, TypeError):
        return False


szerokosc = input("Podaj szerokosc plansz: ") #Wymiar x
while not (war_cal(szerokosc)==True and int(szerokosc)>0): #Sprawdzenie czy szerokosc jest wartoscia calkowita dodatnia
    szerokosc = input("Podano niewlasciwa szerokosc. Podaj liczbe calkowita dodatnia: ")

dlugosc = input("Podaj dlugosc plansz: ") #Wymiar y
while not (war_cal(dlugosc) and int(dlugosc)>0): #Sprawdzenie czy dlugosc jest wartoscia calkowita dodatnia
    dlugosc = input("Podano niewlasciwa dlugosc. Podaj liczbe calkowita dodatnia: ")

miny = input("Podaj liczbe min na planszy: ")
while not (war_cal(miny) and int(miny)>0): #Sprawdzenie czy liczba min jest wartoscia calkowita dodatnia
    miny = input("Podano niewlasciwa liczbe min. Podaj liczbe calkowita dodatnia: ")

szerokosc=int(szerokosc)
dlugosc=int(dlugosc)
miny=int(miny)
strzalx=5
strzaly=2
plansza=gen_plansza(szerokosc,dlugosc,miny,strzalx,strzaly)
for i in range(dlugosc):
    print(plansza[i])
