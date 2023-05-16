import requests




__base_url = 'https://api.gios.gov.pl/pjp-api/rest/'


def get_stations():
    '''
    Request all stations list and return json
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
        return response.json()


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
        return response.json()

#get_index() - trzeba popracować. Funkcja będzie pomocna przy graficznym odwzorowaniu jakosci
#powietrza na mapie. WARTO PRZYSIASC!!!
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
    get_station_sensors('asd')

