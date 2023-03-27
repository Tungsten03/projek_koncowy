from przykladowe_stacje import wszystkie_stacje_pomiarowe as stacje
from geopy import geocoders
from geopy import distance
nl = '\n'
#podaj lokacje
def pobierz_lokalizacje(opis):
    geolocator = geocoders.Nominatim(user_agent='lokacja')
    location = geolocator.geocode(opis)
    koordy  = (location.latitude, location.longitude)
    return koordy

#Funkcja, która tworzy krotki (nazwa stacji, odleglosc)
#nastepnie filtruje po promieniu posortowaną listę
def wskaz_stacje_w_promieniu(koordy_usera, lista_stacji, promien = 50):
    krotki = [(i['stationName'], distance.geodesic(koordy_usera, (float(i['gegrLat']), float(i['gegrLon'])),ellipsoid='GRS-80').km)
              for i in lista_stacji]
    krotki.sort(key=lambda a: a[1])
    return list(filter(lambda odleglosc: promien >= odleglosc[1], krotki))

#kod wykonawczy
opis_lokacji = 'Lusówko, Cienista' #mozna oczywiscie zamienic na input, podane na sztywno dla wygody
koordy_usera = pobierz_lokalizacje(opis_lokacji)
lista_stacji = wskaz_stacje_w_promieniu(koordy_usera, stacje, 120)
print(f"Najbliższe stacje w twojej okolicy (rosnąco) to:")
print(*lista_stacji, sep='\n')