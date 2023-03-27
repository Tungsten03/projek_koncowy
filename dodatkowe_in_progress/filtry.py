# Funkcyjne wersje ćwiczenia 2.1 2.2 i 2.3
# Importy danych
from przykladowe_stacje import wszystkie_stacje_pomiarowe
from przykladowe_stanowiska import wszystkie_stanowiska_stacji_944 as stanowiska
from przykladowe_dane import dane_ze_stanowiska_6087 as dane

# funkcja do filtrowania stacji w wybranym mieście
def stacje_w_miescie(miasto, baza_stacji):
    stacje_w_miescie =  list(filter(lambda stacja: (stacja['city']['name'] == miasto), baza_stacji))
    return list(i['stationName'] for i in stacje_w_miescie)




#Funkcja wypisująca wszystkie stanowiska danej stacji
def stanowiska_w_stacji(lista_stanowisk):
    return [i['param']['paramName'] for i in lista_stanowisk]


# Funkcja do wypisywania wszystkich danych z danego dnia pomiarowego
def dane_z_dnia(data, dane_stacji):
        lista = list(filter(lambda pomiar: data in pomiar['date'], dane_stacji['values']))
        return list(i['value'] for i in lista)

#Czyszczenie danych z None value:
def zmiotka(lista):
    czysta = list(filter(lambda item: item is not None, lista))
    return czysta

#funkcja wyznaczajaca skrajne wartosci danego dnia
def skrajne_dane_dnia(data, dane_stacji, szukany=max):
    """
    arg szukany = min / max
    """
    czysta_lista = zmiotka(dane_z_dnia(data, dane_stacji))
    skrajny_pomiar = szukany(czysta_lista)
    wynik = list(filter(lambda pomiar: pomiar['value'] == skrajny_pomiar, dane_stacji['values']))
    godzina = wynik[0]['date'][12:]
    return (skrajny_pomiar, godzina)

# Funkcja obliczajaca średnią pomiarów niepustych w danym dniu
def wartosc_srednia(data, dane_stacji):
    czysta_lista = zmiotka(dane_z_dnia(data, dane_stacji))
    return sum(czysta_lista)/len(czysta_lista)



print('-'*10, 'stacje w Wa-wie', '-'*10)
stacje_w_wawie = stacje_w_miescie('Warszawa', wszystkie_stacje_pomiarowe)
print(*stacje_w_wawie, sep='\n')

print('-'*10, 'stanowiska w stacji', '-'*10)
wszystkie_stanowiska = stanowiska_w_stacji(stanowiska)
print(*wszystkie_stanowiska, sep='\n')

print('-'*10, 'dane z dnia 2022-10-25', '-'*10)
dane_dnia = dane_z_dnia('2022-10-25', dane)
print(dane_dnia)

print('-'*10, 'dane max z dnia 2022-10-25', '-'*10)
max = skrajne_dane_dnia('2022-10-25', dane)
print(max)

print('-'*10, 'dane min z dnia 2022-10-23', '-'*10)
min = skrajne_dane_dnia('2022-10-23', dane, min)
print(min)

print('-'*10, 'średnia z dnia 2022-10-23', '-'*10)
srednia = wartosc_srednia('2022-10-23', dane)
print(srednia)
