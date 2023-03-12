from peewee import *
from datetime import date
from faker import Faker

fake = Faker()
db = SqliteDatabase('test.db')


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db


db.connect()
Person.drop_table()
Pet.drop_table()
db.create_tables([Person, Pet])

for _ in range(10):
    _ = Person(name=fake.name(), birthday=fake.date())
    _.save()

uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save()
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
grandma.save()
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
bob_kitty.save()

for person in Person.select():
    print(person.name)
