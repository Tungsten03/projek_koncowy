from peewee import *
import start_database as sdb
from api_rest import api_request as r
from utility import utils

# Module contains functions to start and update database
# Uses api_requests module

#Not yet sure if all functions needed.

@utils.time_count #Time-measuring decorator.
def db_add_stations():
    """
    Function that adds station records to database

    :return:
    """
    print('Adding stations to db...')
    stations = r.get_stations()
    for station in stations:
        record = sdb.Station.create(id=station['id'],
                                    stationName=station['stationName'],
                                    gegrLat=station['gegrLat'],
                                    gegrLon=station['gegrLon'],
                                    cityId=station['city']['id'],
                                    cityName=station['city']['name'],
                                    communeName=station['city']['commune']['communeName'],
                                    districtName=station['city']['commune']['districtName'],
                                    provinceName=station['city']['commune']['provinceName'],
                                    addressStreet=station['addressStreet'])
        record.save()
    print('All stations added!')

@utils.time_count
def db_add_sensors():
    """
    Function that adds sensor records to database

    Saving data to db can take around 1 min.

    :return:
    """
    print('adding sensors...')
    for station in sdb.Station.select():
        request_sensor = r.get_station_sensors(station.id)
        for i in request_sensor:
            sensor = sdb.Sensor.create(id=i['id'],
                                   stationId=i['stationId'],
                                   paramName=i['param']['paramName'],
                                   paramFormula=i['param']['paramFormula'],
                                   paramCode=i['param']['paramCode'],
                                   idParam=i['param']['idParam'])
            sensor.save()

    print('sensors added!')

@utils.time_count
def db_add_measurements():
    """
    Function that adds ALL measurements from gios.api to database.
    After that database will be fully completed.
    WARNING!
    Use with caution
    Takes time (up to 4 min)
    For a single sensor measurements use db_add_sensor_measurements()
    :return:
    """
    print('taking measurements...')
    for sensor in sdb.Sensor.select():
        request_value = r.get_sensor_values(sensor.id)
        for i in request_value['values']:
            measurement = sdb.Measurement(sensorId=sensor.id, date=i['date'], value=i['value'])
            measurement.save()

    print('DB READY!')

@utils.time_count
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
        for val in request['values']:
            existing_measurement = sdb.Measurement.get_or_none(sensorId=sensor_id, date=val['date'], value=val['value'])
            if existing_measurement is None:
                measurement = sdb.Measurement.create(sensorId=sensor_id, date=val['date'], value=val['value'])
                measurement.save()
                i+=1
    print(f'{i} records added to database')
@utils.time_count
def update_stations():
    """
    Checks if station already exixst in database if not adds a new record to stations.db

    :return:
    """
    request = r.get_stations()
    i=0
    for station in request:
        existing_station = sdb.Station.get_or_none(stationName=station['stationName'])
        if existing_station is None:
            record = sdb.Station.create(id=station['id'],
                                         stationName=station['stationName'],
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
@utils.time_count
def update_sensors():
    """
    Checks if station already exixst in database if not adds a new record to stations.db

    May take up to 90 seconds

    :return:
    """
    i=0
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

if __name__ == '__main__':
    update_sensors()