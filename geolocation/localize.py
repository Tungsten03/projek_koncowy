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
def stations_in_range(user_place: str, range: int):
    """
    Function takes description of user location (City, street) / (place name e.g. "Uniwersytet Adama Mickiewicza") and prints a list of stations
    in given range (50km by default).

    :user_place: A description of localization given by user
    :range: Search radius in km
    :return: Station in given radius list
    """
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
    Asks the user for a city name and prints a list of stations in that city.

    This function asks user to enter a city name and then retrieves a list of stations in that city from the
    database. It filters the stations based on the provided city name and prints the names of the stations.

    :return: None
    """
    # Ask user for a city name
    city_to_find = input('Podaj nazwę miasta: ').capitalize()
    result = []

    # Set the query and filter stations
    query = sdb.Station.select().where(sdb.Station.cityName == city_to_find)
    for station in query:
        result.append(station.stationName)

    # Print the result:
    if not result:
        print(f'Nie można znaleźć stacji w: {city_to_find}')
    else: print(*result, sep='\n')

# def show_stations_on_map():
#     geopandas.tools.geocode(boros.BoroName, provider='nominatim', user_agent="my-application")
#     import osmnx as ox
#
#     # Pobranie grafu drogowego Polski z OpenStreetMap
#     graph = ox.graph_from_place('Poland', network_type='all')
#
#
#     plt.show()
#
#     # Wczytanie danych z bazy danych
#     query = sdb.Station.select()
#     stations = pd.DataFrame(list(query.dicts()))
#     print(stations)
#
#     # Wczytanie pliku kształtu Polski
#     poland_shapefile = 'path/to/poland_shapefile.shp'
#     poland = gpd.read_file(poland_shapefile)
#
#     # Utworzenie obiektu ramki danych GeoDataFrame
#     geometry = gpd.points_from_xy(stations.gegrLon, stations.gegrLat)
#     stations_gdf = gpd.GeoDataFrame(stations, geometry=geometry)
#
#     # Wyświetlenie stacji na mapie
#     ax = gdf.plot(edgecolor='black', linewidth=0.5)
#     ax.set_axis_off()
#
#     stations_gdf.plot(ax=ax, markersize=5, color='red')
#     plt.show()
## Funckja ma pobierac lokalizacje stacji pomiarowych w polsce i wyswietlac na mapie.
## uzycie bilblioteki geopandass

