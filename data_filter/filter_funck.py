from peewee import *
from database import start_database
from api_rest import api_request as r

db = SqliteDatabase('stations.db', pragmas={'foreign_keys': 1})

if __name__ == '__main__':
    # querry = database.Sensor.select().join(database.Station).where(database.Station.id == '190')
    # for _ in querry:
    #     print(_.paramName)
    db.connect()


    stations =start_database.Station.select()
    for station in stations:
        print(station.stationName, station.id)