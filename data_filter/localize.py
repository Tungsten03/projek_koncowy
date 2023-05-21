import geopy.distance
from geopy import geocoders
from database import start_database as sdb
from utility import utils
import pandas as pd
import webbrowser
import folium


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

@utils.log_exec_time
def show_stations_on_map():
    """
    Function retrieves data from the database and displays them on map.

    Function transforms stations data fetched from SQLite database into
    a pandas dataframe. Folium library is used to create an interactive
    map of Poland.
    Function adds markers on the map according to geolocation data
    and opens a map saved in HTML file in default web browser.

    :return: None
    """
    # Query data from db an make Data Frame
    query = sdb.Station.select()
    df = pd.DataFrame(list(query.dicts()))

    # Create a map centered on Poland
    map = folium.Map(location=[52.2297, 19.0127], zoom_start=5)

    # Add stations points on map
    for index, row in df.iterrows():
        folium.Marker([row['gegrLat'], row['gegrLon']], popup=[row['id'], row['stationName']]).add_to(map)

    # Show the map in a default web browser
    map.save('map.html')
    webbrowser.open('map.html')


