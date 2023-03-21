from peewee import *
from api_rest import api_request as r
from utility import utils

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

@utils.time_count
def db_add_stations():
    print('Adding stations to db...')
    for i in stations:
        station = Station.create(id=i['id'],
                                 stationName=i['stationName'],
                                 gegrLat=i['gegrLat'],
                                 gegrLon=i['gegrLon'],
                                 cityId=i['city']['id'],
                                 cityName=i['city']['name'],
                                 communeName=i['city']['commune']['communeName'],
                                 districtName=i['city']['commune']['districtName'],
                                 provinceName=i['city']['commune']['provinceName'],
                                 addressStreet=i['addressStreet'])
        station.save()
    print('All stations added!')

@utils.time_count
def db_add_sensors():
    print('adding sensors...')
    for station in Station.select():
        request_sensor = r.get_station_sensors(station.id)
        for i in request_sensor:
            sensor = Sensor.create(id=i['id'],
                                   stationId=i['stationId'],
                                   paramName=i['param']['paramName'],
                                   paramFormula=i['param']['paramFormula'],
                                   paramCode=i['param']['paramCode'],
                                   idParam=i['param']['idParam'])
            sensor.save()

    print('sensors added!')

@utils.time_count
def db_add_measurements():
    print('taking measurements...')
    for sensor in Sensor.select():
        request_value = r.get_sensor_values(sensor.id)
        for i in request_value['values']:
            measurement = Measurement(sensorId=sensor.id, date=i['date'], value=i['value'])
            measurement.save()

    print('DB READY!')

if __name__ == '__main__':
    db.connect()

    db.drop_tables([Station, Sensor, Measurement])

    db.create_tables([Station, Sensor, Measurement])


    stations = r.get_stations()

    db_add_stations()
    db_add_sensors()
    db_add_measurements()


