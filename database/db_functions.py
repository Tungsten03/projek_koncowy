import requests
from peewee import *
import start_database as sdb
from api_rest import api_request as r
from utility import utils
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from data_filter import data_analysis as da

db = SqliteDatabase('stations.db')



@utils.log_exec_time #Time-measuring decorator.
def db_add_stations():
    """
    Function that adds station records to the database.

    The function, sets the connection to sqlite3 database 'stations.db',
    retrieves station data from an external API  using the `get_stations()` function from `request` module,
    then creates a table for the `Station` model and inserts the station records into the table.

    NOTE: In case of connection exeptions it connects to database without dropping tables,
    assuming that historical data will be available

    :return: None
    """
    global conection_flag
    print('Adding stations to db...')
    try:
        # Request station list
        stations = r.get_stations()
        # Conect to database
        db.connect()
        # Reset Station Table in database
        db.drop_tables([sdb.Station])
        db.create_tables([sdb.Station])
        # Add data into db
        for station in tqdm(stations):
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
        conection_flag = True
        print('All stations added!')
        return conection_flag
    # Exeption - use the historical data - DO NOT DROP TABLES!
    except (requests.exceptions.HTTPError, requests.ConnectionError):
        db.connect()
        print(f'Wystąpił problem z połączenien. Wczytywanie danych historycznych')
        conection_flag = False
        return conection_flag

def get_sensor_values(sensor_id: int):
    """
        Retrieves sensor values from the GIOS API for a specific sensor.

        This function takes a sensor ID as input and uses it to request sensor values from the GIOS API. The retrieved
        values are then returned.

        Function used in dictionary comprehension in  multithread approach
        for 'db_add_sensor' and 'db_add_measurements' functions.

        :param sensor_id: An integer representing the ID of the sensor.
        :return: The sensor values retrieved from the API.
    """
    return r.get_sensor_values(sensor_id)


@utils.log_exec_time
def db_add_sensors(conection_flag: bool):
    """
    Requests station sensors from an API and adds them to the database.

    This function retrieves sensor data for each station in the database using a multithreaded approach. It makes
    concurrent API requests to fetch the sensor data and then saves the records in the database.

    If the `connection_flag` is True, the function will retrieve sensors from the API and update the database.
    It resets the `Sensors` table in the database before adding new sensors.

    If the `connection_flag` is False, it means there is no connection to the API. Function will skip the sensors
    retrieval process and will not reset the database to make the historical data available.

    :return: None
    """

    if conection_flag:
        print('adding sensors...')
        # Reset Sensor table in database
        db.drop_tables([sdb.Sensor])
        db.create_tables([sdb.Sensor])
        # Setup multithreading and save result in dictionary
        with ThreadPoolExecutor() as executor:
            #Retrieve station sensrors using API for each station in database
            station_sensors = {
                station.id: executor.submit(r.get_station_sensors, station.id)
                for station in sdb.Station.select()
            }


        #iterate through dictionary and save records in database
            for station_id, future in tqdm(station_sensors.items()):
                # Wait fot sensor data
                request_sensor = future.result()
                # Create and save a sensor record in database
                for i in request_sensor:
                    sensor = sdb.Sensor.create(id=i['id'],
                                               stationId=i['stationId'],
                                               paramName=i['param']['paramName'],
                                               paramFormula=i['param']['paramFormula'],
                                               paramCode=i['param']['paramCode'],
                                               idParam=i['param']['idParam'])
                    sensor.save()

        print('sensors added!')
    else:
        print(f'Wczytywanie historycznych danych sensorów')
#

@utils.log_exec_time
def db_add_measurements(conection_flag: bool):
    """
    Adds measurements from the GIOS API to the database for all sensors.

    This function retrieves sensor values from the GIOS API for each sensor in the database using a multithreaded
    approach. It then saves the measurements in the database using bulk create for optimal performance.

    If the `connection_flag` is True, the function will retrieve measurements from the API and update the database.
    It resets the `Measurement` table in the database before adding new measurements. If an exception occurs during
    the process, the `Measurement` table will not be reset.

    If the `connection_flag` is False, it means there is no connection to the API. Function will skip the measurement
    retrieval process and will not drop the table.

    :param conection_flag: A boolean indicating whether to connect to the API and retrieve measurements. Default is True.
    :return: None
    """
    # Check the conection
    if conection_flag:
        print('taking measurements...')

        # Setup multithreading and save result in dictionary
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(get_sensor_values, sensor.id): sensor
                for sensor in sdb.Sensor.select()
            }
            # Reset Sensor table in database
            db.drop_tables([sdb.Measurement])
            db.create_tables([sdb.Measurement])

        # Setup bulk saving
            measurements = []
        # Iterate through futures dictionary and add them into database
        # Bulk create is used for further optimalization
            for future in tqdm(as_completed(futures), total=len(sdb.Sensor.select())):
                values = future.result()
                sensor = futures[future]
                for i in values['values']:
                    measurement = sdb.Measurement(sensorId=sensor.id, date=i['date'], value=i['value'])
                    measurements.append(measurement)
        #batch_size = 200 is 3s faster than default (50)
            sdb.Measurement.bulk_create(measurements, batch_size=200)

        print('Baza danych gotowa!')

    else:
        print('Baza danych gotowa!')


@utils.log_exec_time
def list_stations():
    """
    Prints out all stations saved in the database.

    This function retrieves all stations from the database and prints their IDs and names in ascending order
    based on the city name.

    :return: None
    """
    for station in sdb.Station.select().order_by(sdb.Station.cityName.asc()):
        print(f'{station.id}: {station.stationName}')

@utils.log_exec_time
def sensors_in_station(station: int):
    """
    Prints out all sensors for a given station ID.

    This function retrieves all sensors associated with the provided station ID from the database
    and prints their IDs and parameter codes.

    :param station: An integer representing the station ID.
    :return: None
    """
    query = sdb.Sensor.select().where(sdb.Sensor.stationId == station)

    for sensor in query:
        print(f'{sensor.id}: {sensor.paramCode}')




if __name__ == '__main__':
    #clear log at start



    conection_flag = db_add_stations()
    print(conection_flag)
    db_add_sensors(conection_flag)
    db_add_measurements(conection_flag)

    #
    # # print(localize.stations_in_range('Uniwersytet Adama Mickiewicza, Poznań'))
    # localize.stations_in_city()
    # update_stations()
    list_stations()
    # localize.show_stations_on_map()
    choice = input('podaj id stacji')
    sensors_in_station(choice)
    values = input('podaj id sensora')
    da.highest_measurement(values)
    da.plot_values2(values)


