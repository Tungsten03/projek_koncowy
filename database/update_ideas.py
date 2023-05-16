import requests
import start_database as sdb
from api_rest import api_request as r
from utility import utils
from tqdm import tqdm


@utils.log_exec_time
def update_stations():
    """
    Checks if station already exixsts in database if not adds a new record to stations.db

    :return:
    """
    request = r.get_stations()
    i=0
    for station in tqdm(request):
        existing_station = sdb.Station.get_or_none(stationName=station['stationName'])
        if existing_station is None:
            record = sdb.Station.create(id=station['id'],
                                         stationName=station['stationName'].replace('ul. ', ''),
                                         gegrLat=station['gegrLat'],
                                         gegrLon=station['gegrLon'],
                                         cityId=station['city']['id'],
                                         cityName=station['city']['name'],
                                         communeName=station['city']['commune']['communeName'],
                                         districtName=station['city']['commune']['districtName'],
                                         provinceName=station['city']['commune']['provinceName'],
                                         addressStreet=station['addressStreet'])
            record.save()
            i+=1
    print(f'{i} stations added to database')
@utils.log_exec_time
def update_sensors():
    """
    Checks if station already exixst in database if not adds a new record to stations.db

    May take up to 90 seconds

    :return:
    """
    i=0
    try:
        for station in sdb.Station.select():
            request = r.get_station_sensors(station.id)
            for sensor in request:
                existing_sensor = sdb.Sensor.get_or_none(id=sensor['id'])
                if existing_sensor is None:
                    record = sdb.Sensor.create(id=sensor['id'],
                                               stationId=sensor['stationId'],
                                               paramName=sensor['param']['paramName'],
                                               paramFormula=sensor['param']['paramFormula'],
                                               paramCode=sensor['param']['paramCode'],
                                               idParam=sensor['param']['idParam'])
                    record.save()
                    i+=1
        print(f'{i} sensors added to database')
    except requests.exceptions.HTTPError:
        print('Brak połączenia z API GIOŚ. będziesz używał pomiarów historycznych z bazy danych.')

@utils.log_exec_time
def db_add_sensor_measurements(sensor_id):
    """
    Request all measurements for specified station id
    adds a record to db if measurement not in db.

    Function will count and print a prompt of saved records quantity.

    If no parameter values were measured will return a warning.

    Example: db_add_sensor_measurements(644)

    :param sensor_id: int
    :return: str
    """
    print('Requesting values. May take up to 1,5 min...')
    request = r.get_sensor_values(sensor_id)
    i=0
    if not request['values']:
        print('selected sensor measured no parameter values')
    else:
        for val in tqdm(request['values']):
            existing_measurement = sdb.Measurement.get_or_none(sensorId=sensor_id, date=val['date'], value=val['value'])
            if existing_measurement is None:
                measurement = sdb.Measurement.create(sensorId=sensor_id, date=val['date'], value=val['value'])
                measurement.save()
                i+=1
    print(f'{i} records added to database')



