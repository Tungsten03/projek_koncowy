import requests

__base_url = 'https://api.gios.gov.pl/pjp-api/rest/'


def get_stations():
    """
    Request list of all stations

    Function uses get method to request a list of stations from GIOS API and returns
    the response in JSON format.

    :return: JSON
    """
    # Set headers to json
    headers = {'Accept': 'application/json'}
    # Build URL to request all stations from API
    url = __base_url + 'station/findAll'
    # Send a GET request to API GIOS
    response = requests.get(url=url, headers=headers)
    # HTTP exceptions handling
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    else:
        return response.json()


def get_station_sensors(station_id: int):
    """
    Request all sensors fora specific station

    Function takes station ID as a parameterm, sends request do GIOS API and returns respond in JSON format

    :param station_id: the ID of a station
    :return: JSON response
    """
    # Set headers to json
    headers = {'Accept': 'application/json'}
    # Build URL to request all sensors from API
    url = f'{__base_url}station/sensors/{station_id}'
    # Send a GET request to API GIOS
    response = requests.get(url=url, headers=headers)
    # HTTP exceptions handling
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    else:
        if not response.json():
            print(f'Station with id number: {station_id} does not exist.')
        else:
            return response.json()


def get_sensor_values(sensor_id: int):
    """
      Request collected data values for a specific sensor ID.

      This function sends a request to the GIOS API to retrieve collected data values for the specified sensor ID.
      It returns the response in JSON format.

      :param sensor_id: An integer representing the ID of the sensor.
      :return: JSON response containing collected data values for the sensor.
      """
    # Set headers to json
    headers = {'Accept': 'application/json'}
    # Build URL to request all measurements from API
    url = f'{__base_url}data/getData/{sensor_id}'
    # Send a GET request to API GIOS
    response = requests.get(url=url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    else:
        return response.json()

# get_index() - trzeba popracować. Funkcja będzie pomocna przy graficznym odwzorowaniu jakosci
# powietrza na mapie. WARTO PRZYSIASC!!!
# def get_index(station_id: int, param_key: str):
#     '''
#     Retrieves sensor values from the GIOS API for a specific sensor.
#
#     This function takes a sensor ID as input and uses it to request sensor values from the GIOS API. The retrieved
#     values are then returned.
#
#     :param sensor_id: An integer representing the ID of the sensor.
#     :return: The sensor values retrieved from the API.
#     '''
#     headers = {'Accept': 'application/json'}
#
#     url = f'{__base_url}aqindex/getIndex/{station_id}'
#     response = requests.get(url=url, headers=headers)
#     try:
#         response.raise_for_status()
#     except requests.exceptions.HTTPError as error:
#         print(error)
#     else:
#         if not response.json():
#             print(f'iii')
#         else:
#             try:
#                 print(response.json()[f'{param_key}IndexLevel']['indexLevelName'])
#             except KeyError:
#                 print('There is no such parameter')
