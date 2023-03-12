from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import *
import json
from api_rest import request as r

db = SqliteDatabase('stations.db')


class Station(Model):
    id = CharField(null='False')
    stationName = CharField(null='False')
    gegrLat = CharField(null='False')
    gegrLon = CharField(null='False')
    city = CharField(null='False')
    addressStreet = CharField(null='False')

    class Meta:
        database = db


class Sensor(Station):
    id = CharField()
    stationId = ForeignKeyField(Station, backref='sensors')
    paramName = CharField(null='False')
    paramFormula = CharField(null='False')
    paramCode = CharField(null='False')
    idParam = CharField()



if __name__ == '__main__':
    db.connect()
    Station.drop_table()
    Sensor.drop_table()
    db.create_tables([Station, Sensor])

    with open('station_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for i in data:
            station = Station.create(id=i['id'],
                                     stationName=i['stationName'],
                                     gegrLat=i['gegrLat'],
                                     gegrLon=i['gegrLon'],
                                     city=i['city']['name'],
                                     addressStreet=i['addressStreet'])
            station.save()

    for station in Station.select():
        req = r.get_station_sensors(station.id)
        for i in req:
            sensor = Sensor.create(id=i['id'],
                                   stationId=i['stationId'],
                                   paramName=i['param']['paramName'],
                                   paramFormula=i['param']['paramFormula'],
                                   paramCode=i['param']['paramCode'],
                                   idParam=i['param']['idParam']
                                   )
            sensor.save()
