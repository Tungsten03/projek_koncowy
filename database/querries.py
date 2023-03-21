from peewee import *
import database
from api_rest import api_request as r

db = SqliteDatabase('stations.db', pragmas={'foreign_keys': 1})

if __name__ == '__main__':
    # querry = database.Sensor.select().join(database.Station).where(database.Station.id == '190')
    # for _ in querry:
    #     print(_.paramName)

    for sensor in database.Sensor.select():
        request_value = r.get_sensor_values(sensor.id)
        for _ in request_value['values']:
            print(repr(_['value']))