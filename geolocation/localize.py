import geopy.distance
from geopy import geocoders
from database import start_database as sdb
from utility import utils
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

#Set the geolocator
geolocator = geocoders.Nominatim(user_agent='lokacja')


def get_coords(descritpion):
    if not descritpion:
        print(descritpion)
    else:
        location = geolocator.geocode(descritpion)
        return (location.latitude, location.longitude)



@utils.log_exec_time
def stations_in_range(user_place, range=10):
    """
    Function takes description of user location (City, street) / (place name e.g. "Uniwersytet Adama Mickiewicza") and prints a list of stations
    in given range (50km by default).

    :return: str
    """
    # #get data from user
    # user_place = input('Podaj opis swojej lokalizacji w formacie: Miasto, ulica lub: Nazwa własna miejsca')
    # range = float(input('Wskaż promień poszukiwań (w km)'))

    #get user location
    user_location = geolocator.geocode(user_place)
    user_coords = (user_location.latitude, user_location.longitude)

    station_list = []

    #search station in range and save in list
    for station in sdb.Station.select():
        station_location = (station.gegrLat, station.gegrLon)
        user_distance = geopy.distance.distance(user_coords, station_location)
        if user_distance <= range:
            station_list.append((station.id, station.stationName))
    return station_list

@utils.log_exec_time
def stations_in_city():
    """
    Function asks for a city name and prints out a list of stations in it.

    :return:
    """
    #Ask user for a city name
    city_to_find = input('Podaj nazwę miasta: ').capitalize()
    result = []

    #set the query and filter stations
    query = sdb.Station.select().where(sdb.Station.cityName == city_to_find)
    for station in query:
        result.append(station.stationName)

    #print the result:
    if not result:
        print(f'Nie można znaleźć stacji w: {city_to_find}')
    else: print(*result, sep='\n')

def show_stations_on_map():

    # Wczytanie danych z bazy danych
    query = sdb.Station.select()
    stations = pd.DataFrame(list(query.dicts()))
    print(stations)

    # Utworzenie obiektu ramki danych GeoDataFrame
    geometry = gpd.points_from_xy(stations.gegrLon, stations.gegrLat)
    stations_gdf = gpd.GeoDataFrame(stations, geometry=geometry)

    # Wyświetlenie stacji na mapie
    stations_gdf.plot()
## Funckja ma pobierac lokalizacje stacji pomiarowych w polsce i wyswietlac na mapie.
## uzycie bilblioteki geopandass