import random
import os
import sys
import msvcrt

KOLORY = {
    'ZIELONY': "\033[92m",
    'CZERWONY': "\033[91m",
    'NIEBIESKI': "\033[94m",
    'FIOLETOWY': "\033[95m",
    'RESET': "\033[0m",
    'ZOLTY': "\033[93m",
    'POMARANCZOWY': "\033[33m"
}

ZNAKI = {
    'NIEODKRYTY': ".",
    'PUSTE': " ",
    'MINA': "*",
    'FLAGA': "F"

}

def gen_plansza(x,y,z,stX,stY):
    mapa=[[0 for _ in range(x)] for _ in range(y)]
    mapa[stY][stX]='O'
    postawione_miny=0
    while postawione_miny < z: #Generowanie min (miny oznaczone 'X')
        minaX=random.randint(0,x-1)
        minaY=random.randint(0,y-1)

        if mapa[minaY][minaX]!='X' and not ((abs(stX - minaX) <= 1) and (abs(stY - minaY) <=1)):
            mapa[minaY][minaX]='X'
            postawione_miny+=1

    # Przypisywanie wartosci pol (liczenie sąsiadów)
    for i in range(y): 
        for j in range(x):
            if mapa[i][j] == 'X': continue # Jeśli mina, to nie liczymy
            
            licznik = 0
            # Sprawdzanie 3x3
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if ((i + k >= 0) and (j + l >= 0)):
                        if ((i + k <= y - 1) and (j + l <= x - 1)):
                            if (mapa[i + k][j + l] == 'X'):
                                licznik = licznik + 1
            mapa[i][j] = licznik

    return mapa


def war_cal(x): #Sprawdzenie czy podana liczba jest calkowita
    try:
        int(x)
        return True
    except (ValueError, TypeError):
        return False

def ilosc_min(miny,max_miny):
    try:
        wartosc = int(miny)
        if wartosc > 0 and wartosc <= max_miny :
            return True
        else:
            return False
    except (ValueError, TypeError):
        return False

def wybierz_pole(szerokosc, wysokosc):
    kursor = [0, 0] 

    while True:
        #czyszczenie ekranu
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"SAPER | ODKRYJ PIERWSZE POLE | ENTER-ODKRYJ")
        print("-" * (szerokosc * 3 + 2))

        #rysowanie planszy 
        for y in range(wysokosc):
            linia = ""
            for x in range(szerokosc):
                znak = ZNAKI['NIEODKRYTY']  
                #rysowanie kursora
                if x == kursor[0] and y == kursor[1]:
                    linia += f"[{znak}]"
                else:
                    linia += f" {znak} "
            print(f"{KOLORY['ZIELONY']}{linia}{KOLORY['RESET']}")

        #Obsluga klawiszy 
        klawisz = msvcrt.getch()

        if klawisz == b'\xe0': # STRZALKI
            strzalka = msvcrt.getch()
            if strzalka == b'H':   kursor[1] = max(0, kursor[1] - 1)          #gora
            elif strzalka == b'P': kursor[1] = min(wysokosc - 1, kursor[1] + 1) #dol
            elif strzalka == b'K': kursor[0] = max(0, kursor[0] - 1)          #lewo
            elif strzalka == b'M': kursor[0] = min(szerokosc - 1, kursor[0] + 1) #prawo
        
        elif klawisz == b'\r': # ENTER
            # wspolrzedne startowe
            return kursor[0], kursor[1]

def rysuj_plansze(szerokosc, wysokosc, mapa, odkryte, flagi, kursor, miny_total, koniec=False):
    "rysowanie wlasciwej planszy podczas gry"
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"MINY: {miny_total - len(flagi)} | STRZALKI-RUCH | SPACJA-FLAGA | ENTER-ODKRYJ")
    print("-" * (szerokosc * 3 + 2))

    for y in range(wysokosc) :
        linia=""
        for x in range(szerokosc) :
            znak = ZNAKI['NIEODKRYTY'] 
            kolor = KOLORY['ZIELONY']
            if koniec and mapa[y][x]=='X': #koniec gry
                znak = ZNAKI['MINA']
                kolor = KOLORY['CZERWONY']
            elif (x,y) in flagi: #flaga
                znak = ZNAKI['FLAGA']
                kolor = KOLORY['CZERWONY']
            elif (x, y) in odkryte: #odkryte pole
                wartosc=mapa[y][x]
                if wartosc==0:
                    znak = ZNAKI['PUSTE']
                    kolor = KOLORY['RESET']
                else:
                    znak = str(wartosc)
                    if wartosc == 1 : kolor=KOLORY['NIEBIESKI']
                    elif wartosc == 2 : kolor=KOLORY['ZOLTY']
                    elif wartosc == 3 : kolor=KOLORY['POMARANCZOWY']
                    else : kolor=KOLORY['FIOLETOWY']
        
            if x == kursor[0] and y == kursor[1]:
                linia += f"[{kolor}{znak}{KOLORY['RESET']}]"
            else:
                linia += f" {kolor}{znak}{KOLORY['RESET']} "
        print(linia)
    

def odkrywanie_rek(x,y,mapa,odkryte,szerokosc,wysokosc):
    if(x,y) in odkryte: return 0
    if not (0<=x<szerokosc and 0<=y<wysokosc): return
    
    odkryte.add((x,y))

    if mapa[y][x] == 0 : 
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0 : continue 
                odkrywanie_rek(x+j, y+i, mapa, odkryte, szerokosc, wysokosc)



def main():
    
    
    
    

    szerokosc = input("Podaj szerokosc plansz: ") #Wymiar x
    while not (war_cal(szerokosc)==True and int(szerokosc)>0): #Sprawdzenie czy szerokosc jest wartoscia calkowita dodatnia
        szerokosc = input("Podano niewlasciwa szerokosc. Podaj liczbe calkowita dodatnia: ")

    dlugosc = input("Podaj dlugosc plansz: ") #Wymiar y
    while not (war_cal(dlugosc) and int(dlugosc)>0): #Sprawdzenie czy dlugosc jest wartoscia calkowita dodatnia
        dlugosc = input("Podano niewlasciwa dlugosc. Podaj liczbe calkowita dodatnia: ")

    max_min=(int(szerokosc)*int(dlugosc))-9
    miny = input(f"Podaj liczbe min na planszy (maksymalnie {max_min}): ")
    while not (ilosc_min(miny, max_min)) : #Sprawdzenie czy liczba min jest wartoscia calkowita dodatnia
        miny = input(f"Podano niewlasciwa liczbe min. Podaj liczbe calkowita dodatnia nieprzekraczajaca {max_min}: ")

    szerokosc=int(szerokosc)
    dlugosc=int(dlugosc)
    miny=int(miny)
    start_x, start_y=wybierz_pole(szerokosc,dlugosc)  #wybor pola startowego
    plansza=gen_plansza(szerokosc,dlugosc,miny,start_x,start_y) #generowanie planszy

    flagi=set()
    odkryte=set()
    kursor=[start_x,start_y]
    
    odkrywanie_rek(start_x, start_y, plansza, odkryte, szerokosc, dlugosc) #odkrywanie pierwszego pola

    gra_trwa=True
    while gra_trwa :
        rysuj_plansze(szerokosc, dlugosc, plansza, odkryte, flagi, kursor, miny)


        if len(odkryte) == (szerokosc * dlugosc) - miny:
            print(f"\n{KOLORY['ZIELONY']}WSZYSTKIE MINY ZOSTALY ODKRYTE{KOLORY['RESET']}")
            gra_trwa= False

        klawisz = msvcrt.getch()

        if klawisz == b'\xe0': #strzalki
            strzalka = msvcrt.getch()
            if strzalka == b'H':   kursor[1] = max(0, kursor[1] - 1)
            elif strzalka == b'P': kursor[1] = min(dlugosc - 1, kursor[1] + 1)
            elif strzalka == b'K': kursor[0] = max(0, kursor[0] - 1)
            elif strzalka == b'M': kursor[0] = min(szerokosc - 1, kursor[0] + 1)
        
        elif klawisz == b' ': #spacja - flaga
            pozycja = (kursor[0], kursor[1])
            if pozycja not in odkryte:
                if pozycja in flagi:
                    flagi.remove(pozycja)
                else:
                    flagi.add(pozycja)
        
        elif klawisz == b'\r': #enter - odkryj
            pozycja = (kursor[0], kursor[1])
            
            
            if pozycja in flagi: continue 
            
            if plansza[kursor[0]][kursor[1]] == 'X':
                rysuj_plansze(szerokosc, dlugosc, plansza, odkryte, flagi, kursor, miny, koniec=True)
                print(f"\n{KOLORY['CZERWONY']}TRAFILES NA MINE{KOLORY['RESET']}")
                gra_trwa = False
            else:
                odkrywanie_rek(kursor[0], kursor[1], plansza, odkryte, szerokosc, dlugosc)

        elif klawisz == b'q':
            gra_trwa = False




if __name__ == "__main__":
    main()

