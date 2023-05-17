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





