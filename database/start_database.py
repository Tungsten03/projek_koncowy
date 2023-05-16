from peewee import *


db = SqliteDatabase('stations.db')


class BaseModel(Model):
    class Meta:
        database = db

class Station(BaseModel):
    id = IntegerField()
    stationName = CharField()
    gegrLat = CharField()
    gegrLon = CharField()
    cityId = IntegerField()
    cityName = CharField()
    communeName = CharField()
    provinceName = CharField()
    addressStreet = CharField(null=True)


class Sensor(BaseModel):
    id = IntegerField()
    stationId = ForeignKeyField(Station, backref='sensors')
    paramName = CharField()
    paramFormula = CharField()
    paramCode = CharField()
    idParam = CharField()


class Measurement(BaseModel):
    sensorId = ForeignKeyField(Sensor, backref='measurements')
    date = CharField()
    value = FloatField(null=True)
#
# @utils.time_count
# def db_add_stations():
#     print('Adding stations to db...')
#     stations = r.get_stations()
#     for i in stations:
#         station = Station.create(id=i['id'],
#                                  stationName=i['stationName'],
#                                  gegrLat=i['gegrLat'],
#                                  gegrLon=i['gegrLon'],
#                                  cityId=i['city']['id'],
#                                  cityName=i['city']['name'],
#                                  communeName=i['city']['commune']['communeName'],
#                                  districtName=i['city']['commune']['districtName'],
#                                  provinceName=i['city']['commune']['provinceName'],
#                                  addressStreet=i['addressStreet'])
#         station.save()
#     print('All stations added!')
#
# @utils.time_count
# def db_add_sensors():
#     print('adding sensors...')
#     for station in Station.select():
#         request_sensor = r.get_station_sensors(station.id)
#         for i in request_sensor:
#             sensor = Sensor.create(id=i['id'],
#                                    stationId=i['stationId'],
#                                    paramName=i['param']['paramName'],
#                                    paramFormula=i['param']['paramFormula'],
#                                    paramCode=i['param']['paramCode'],
#                                    idParam=i['param']['idParam'])
#             sensor.save()
#
#     print('sensors added!')
#
# @utils.time_count
# def db_add_measurements():
#     print('taking measurements...')
#     for sensor in Sensor.select():
#         request_value = r.get_sensor_values(sensor.id)
#         for i in request_value['values']:
#             measurement = Measurement(sensorId=sensor.id, date=i['date'], value=i['value'])
#             measurement.save()
#
#     print('DB READY!')
#
# @utils.time_count
# def db_add_sensor_measurements(sensor_id):
#     """
#     Request all measurements for specified station id
#     and add record to db if measurement not in db.
#
#     Function will count and print a prompt of saved records quantity.
#
#     If no parameter values were measured will return a warning.
#
#     Example: db_add_sensor_measurements(644)
#
#     :param sensor_id: int
#     :return: str
#     """
#     print('Requesting values. May take up to 1,5 min...')
#     request = r.get_sensor_values(sensor_id)
#     i=0
#     if not request['values']:
#         print('selected sensor measured no parameter values')
#     else:
#         for val in request['values']:
#             existing_measurement = Measurement.get_or_none(sensorId=sensor_id, date=val['date'], value=val['value'])
#             if existing_measurement is None:
#                 measurement = Measurement.create(sensorId=sensor_id, date=val['date'], value=val['value'])
#                 measurement.save()
#                 i+=1
#     print(f'{i} records added to database')


if __name__ == '__main__':
    db.connect()

    stations = Station.select()
    for station in stations:
        print(station.stationName, station.id)



