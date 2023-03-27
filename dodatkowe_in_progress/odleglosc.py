from geopy import distance

# Funkcje obliczające odległość między lokacjami
def zrob_krotke(miejscowosc):
        return tuple(float(item) for item in miejscowosc.split())

if __name__ == '__main__':
    print('program policzy odleglosci miedzy dwiema miejscowosciami')
    print('wymagany format: xx,xxx yy,yyy')
    print('gdzie x to dlugosc a y to szerokosc')
    pierwsza = input('podaj lokalizacje pierwszej miejscowosci:')
    druga = input('podaj lokalizacje drugiej miejscowosci:')
    try:
        pierwsza =  zrob_krotke(pierwsza)
        druga = zrob_krotke(druga)


    except ValueError:
        print('Podano zły format lokalizacji')

    try:
        print(repr(pierwsza))
    except NameError:
        print('Przerwano prace programu')

    odleglosc = distance.great_circle(pierwsza, druga).km
    print(f'ogległosc miedzy miejscowosciami wynosi: {odleglosc} km')
    odleglosc2 = distance.geodesic(pierwsza,druga,ellipsoid='GRS-80').km
    print(f'ogległosc geodezyjna miedzy miejscowosciami wynosi: {odleglosc2} km')

