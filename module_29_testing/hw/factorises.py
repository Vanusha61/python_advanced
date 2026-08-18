import random
import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from .model import Client, Parking, db

fake = Faker()

class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyFunction(
        lambda: fake.credit_card_number() if random.choice([True, False]) else None
    )
    car_number = factory.Faker('license_plate')

class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('street_address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=1, max=100)
    count_available_places = factory.LazyAttribute(lambda o: o.count_places)