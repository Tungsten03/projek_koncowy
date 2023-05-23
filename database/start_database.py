"""
SQLite Database Models using Peewee ORM.

This module defines the database models for SQLite using the Peewee ORM.

Classes:

- BaseModel: Base model class for Peewee models.
- Station: Represents a station in the database.
- Sensor: Represents a sensor in the database.
- Measurement: Represents a measurement in the database.

Dependencies:

- Peewee: Python ORM for SQLite.
"""

from peewee import *

db = SqliteDatabase('stations.db')


class BaseModel(Model):
    """
    Base model class for Peewee models
    """
    class Meta:
        database = db

class Station(BaseModel):
    """
    Model representing a station in the database.

    This model defines the fields and relationships for a station. It includes fields
    that correspond to the columns in the 'station' table in the database.

    """
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
    """
    Model representing a sensor in the database.

    This model defines the fields and relationships for a sensor. It includes fields
    that correspond to the columns in the 'sensor' table in the database.
    The `stationId` field is a foreign key referencing the `Station` model.
    """
    id = IntegerField()
    stationId = ForeignKeyField(Station, backref='sensors')
    paramName = CharField()
    paramFormula = CharField()
    paramCode = CharField()
    idParam = CharField()


class Measurement(BaseModel):
    """
    Model representing a measurement in the database.

    This model defines the fields and relationships for a measurement. It includes fields
    that correspond to the columns in the 'measurement' table in the database.
    The `sensorId` field is a foreign key referencing the `Sensor` model.
    """
    sensorId = ForeignKeyField(Sensor, backref='measurements')
    date = CharField()
    value = FloatField(null=True)





