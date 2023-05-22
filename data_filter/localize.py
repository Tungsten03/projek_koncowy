"""
Module for Geographic Operations and Visualization.

This module provides functions for geolocation operations and visualization of station data on a map.

Functions:

    check server() -> bool: Check openstreetmap server status.
    of a given location description.
    stations_in_range(user_place: str, range: int) -> List: Retrieves a list of stations within
    a given range (in km) from a user-defined location.
    stations_in_city(): Asks the user for a city name and prints a list of stations in that city.
    show_stations_on_map(): Retrieves station data from the database and displays them on a map.
"""

import geopy.distance
from geopy import geocoders
from database import start_database as sdb
from utility import utils
import pandas as pd
import webbrowser
import folium
import requests
import tkinter as tk
from utility import labels as lbl


#Set the geolocator
geolocator = geocoders.Nominatim(user_agent='lokacja')

def check_server() -> bool:
    """
    Check nominatim server status
    :return: Bool
    """
    server_url = 'https://nominatim.openstreetmap.org/status.php'

    try:
        response = requests.head(server_url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False


# def get_coords(descritpion):
#     if not descritpion:
#         print(descritpion)
#     else:
#         location = geolocator.geocode(descritpion)
#         return (location.latitude, location.longitude)



@utils.log_exec_time
def stations_in_range(user_place: str, range: int) -> list[tuple[int, str]]:
    """
    Function takes description of user location (City, street) / (place name e.g. "Uniwersytet Adama Mickiewicza") and prints a list of stations
    in given range (50km by default).

    At start function check_server() will check openstreetmap server status. In case of any connection issues a popup
    window with warning is displayed.

    :user_place: A description of localization given by user
    :range: Search radius in kilometers
    :return: A list of tuples representing the stations within the specified range. Each tuple contains the station ID
             and station name.
    """
    # Check openstreetmap server status
    if not check_server():
        # Display a popup window if server is down
        popup = tk.Toplevel()
        popup.title('Uwaga!')

        label = tk.Label(popup, text=lbl.popup_connect)
        label.pack(padx=20, pady=20)

        button = tk.Button(popup, text="Zamknij", command=popup.destroy)
        button.pack(pady=10)
    else:
        # Get user location
        user_location = geolocator.geocode(user_place)
        user_coords = (user_location.latitude, user_location.longitude)

        station_list = []

        # Search station in range and save in list
        for station in sdb.Station.select():
            station_location = (station.gegrLat, station.gegrLon)
            user_distance = geopy.distance.distance(user_coords, station_location)
            if user_distance <= range:
                station_list.append((station.id, station.stationName))
        return station_list

@utils.log_exec_time
def stations_in_city() -> None:
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
def show_stations_on_map() -> None:
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


