from peewee import *
import database

db = SqliteDatabase('stations.db', pragmas={'foreign_keys': 1})

if __name__ == '__main__':
    querry = database.Sensor.select().join(database.Station).where(database.Station.id == '190')
    for _ in querry:
        print(_.paramName)