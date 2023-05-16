from peewee import *
from database import start_database as sdb
from api_rest import api_request as r

db = SqliteDatabase('stations.db')

if __name__ == '__main__':
    # querry = database.Sensor.select().join(database.Station).where(database.Station.id == '190')
    # for _ in querry:
    #     print(_.paramName)
    db.connect()


    stations =sdb.Station.select()
    for station in stations:
        print(station.stationName, station.id)