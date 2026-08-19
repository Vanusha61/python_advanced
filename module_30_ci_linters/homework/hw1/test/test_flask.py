from datetime import datetime

import pytest


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_all_get_good_200(client, route):
    response = client.get(route)
    assert response.status_code == 201


def test_create_good_client_201(client):
    data = {
        "name": "name1",
        "surname": "surname1",
        "credit_card": "123123123",
        "car_number": "123123123",
    }
    response = client.post("/clients", json=data)
    result = {
        "client": {
            "car_number": "123123123",
            "credit_card": "123123123",
            "id": 2,
            "name": "name1",
            "surname": "surname1",
        }
    }
    assert response.status_code == 201
    assert response.get_json() == result


def test_create_good_parking_201(client):
    data = {
        "address": "123123123",
        "opened": True,
        "count_places": 3,
        "count_available_places": 3,
    }
    response = client.post("/parkings", json=data)
    result = {
        "parking": {
            "address": "123123123",
            "count_available_places": 3,
            "count_places": 3,
            "id": 2,
            "opened": True,
        }
    }
    assert response.status_code == 201
    assert response.get_json() == result


@pytest.mark.parking
def test_create_good_client_parking_201(client):
    data_client = {
        "name": "name1",
        "surname": "surname1",
        "credit_card": "123123123",
        "car_number": "123123123",
    }
    response_client = client.post("/clients", json=data_client)
    clients_id = response_client.get_json()["client"]["id"]

    data_parking = {
        "address": "123123123",
        "opened": True,
        "count_places": 3,
        "count_available_places": 3,
    }
    response_parking = client.post("/parkings", json=data_parking)
    parking_id = response_parking.get_json()["parking"]["id"]

    data = {
        "client_id": clients_id,
        "parking_id": parking_id,
        "time_in": datetime.now(),
    }
    response = client.post("client_parkings", json=data)
    result = {
        "client_parking": {
            "client_id": 2,
            "id": 2,
            "parking_id": 2,
            "time_in": f"{response.get_json()['client_parking']['time_in']}",
            "time_out": None,
        }
    }
    assert response.status_code == 201
    assert response.get_json() == result


@pytest.mark.parking
def test_delete_good_client_parking_200(client):
    data_client = {
        "name": "name1",
        "surname": "surname1",
        "credit_card": "123123123",
        "car_number": "123123123",
    }
    response_client = client.post("/clients", json=data_client)
    clients_id = response_client.get_json()["client"]["id"]

    data_parking = {
        "address": "123123123",
        "opened": True,
        "count_places": 3,
        "count_available_places": 3,
    }
    response_parking = client.post("/parkings", json=data_parking)
    parking_id = response_parking.get_json()["parking"]["id"]

    data_client_parking = {
        "client_id": clients_id,
        "parking_id": parking_id,
        "time_in": datetime.now(),
    }
    response = client.post("client_parkings", json=data_client_parking)

    data = {
        "client_id": clients_id,
        "parking_id": parking_id,
    }
    response = client.delete("/client_parkings", json=data)
    result = {"delete": True}
    assert response.status_code == 200
    assert response.get_json() == result
