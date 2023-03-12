import requests
import json




__base_url = 'https://api.gios.gov.pl/pjp-api/rest/'


def get_stations():
    '''
    Request all stations list and save to json file
    :return: json
    '''
    headers = {'Accept': 'application/json'}

    url = __base_url + 'station/findAll'
    response = requests.get(url=url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    else:
        with open('station_list.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, ensure_ascii=False)

def get_station_sensors(station_id: int):
    '''
    Request all sensors for station
    :param station_id: int
    :return: json
    '''
    headers = {'Accept': 'application/json'}

    url = f'{__base_url}station/sensors/{station_id}'
    response = requests.get(url=url, headers=headers)
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
    '''

    Request collected data values for sensor id
    :param sensor_id: int
    :return: json
    '''
    headers = {'Accept': 'application/json'}

    url = f'{__base_url}data/getData/{sensor_id}'
    response = requests.get(url=url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    else:
        if not response.json()['values']:
            print(f'Sensor number: {sensor_id} has no data')
        else:
            return response.json()['values']

def get_index(station_id: int, param_key: str):
    '''
    Request an index level of measured parameter.
    :param station_id: int
    :param param_key: str
    :return:
    '''
    headers = {'Accept': 'application/json'}

    url = f'{__base_url}aqindex/getIndex/{station_id}'
    response = requests.get(url=url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    else:
        if not response.json():
            print(f'iii')
        else:
            try:
                print(response.json()[f'{param_key}IndexLevel']['indexLevelName'])
            except KeyError:
                print('There is no such parameter') #Popracować nad alertem



if __name__ == '__main__':

    with open('station_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        sensors = []
        with open('sensor_list.json', 'w', encoding='utf-8') as sens:
            for station in data:
                sensor = get_station_sensors(station['id'])
                sensors.append(sensor)
                print(station['id'])
            json.dump(sensors, sens)


