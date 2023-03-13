from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import *
import json
from api_rest import request as r

db = SqliteDatabase('stations.db')


class Model(Model):
    class Meta:
        database = db

class Station(Model):
    id = IntegerField(null='False')
    stationName = CharField(null='False')
    gegrLat = CharField(null='False')
    gegrLon = CharField(null='False')
    city = CharField(null='False')
    addressStreet = CharField(null='False')



class Sensor(Station):
    id = IntegerField()
    stationId = ForeignKeyField(Station, backref='sensors')
    paramName = CharField(null='False')
    paramFormula = CharField(null='False')
    paramCode = CharField(null='False')
    idParam = CharField()




if __name__ == '__main__':
    db.connect()
    db.drop_tables([Model, Station, Sensor])

    db.create_tables([Model, Station, Sensor])


    stations = r.get_stations()
    for i in stations:
        station = Station.create(id=i['id'],
                                 stationName=i['stationName'],
                                 gegrLat=i['gegrLat'],
                                 gegrLon=i['gegrLon'],
                                 city=i['city']['name'],
                                 addressStreet=i['addressStreet'])
        station.save()

    for station in Station.select():
        request_sensor = r.get_station_sensors(station.id)
        for i in request_sensor:
            sensor = Sensor.create(id=i['id'],
                                   stationId=i['stationId'],
                                   paramName=i['param']['paramName'],
                                   paramFormula=i['param']['paramFormula'],
                                   paramCode=i['param']['paramCode'],
                                   idParam=i['param']['idParam']
                                   )
            sensor.save()


