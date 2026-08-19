from datetime import datetime, timedelta

from module_30_ci_linters.homework.hw1 import create_app
from module_30_ci_linters.homework.hw1.model import Client, ClientParking, Parking
from module_30_ci_linters.homework.hw1.model import db as _db
from pytest import fixture


@fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.drop_all()
        _db.create_all()
        client = Client(
            id=1,
            name="name",
            surname="surname",
            credit_card="credit_card",
            car_number="123456789",
        )
        parking = Parking(
            id=1,
            address="address",
            opened=True,
            count_places=3,
            count_available_places=3,
        )
        client_parking = ClientParking(
            id=1,
            client_id=1,
            parking_id=1,
            time_in=datetime.now(),
            time_out=datetime.now() + timedelta(hours=2),
        )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app


@fixture
def client(app):
    client = app.test_client()
    yield client


@fixture
def db(app):
    with app.app_context():
        yield _db
