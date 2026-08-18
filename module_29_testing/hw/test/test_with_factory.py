from module_29_testing.hw.factorises import ClientFactory, ParkingFactory


def test_create_client(app, db, client):
    client_data = ClientFactory()
    response = client.post('/clients', json={
        'name': client_data.name,
        'surname': client_data.surname,
        'credit_card': client_data.credit_card,
        'car_number': client_data.car_number
    })
    assert response.status_code == 201


def test_create_parking(app, db, client):
    parking = ParkingFactory()
    response = client.post('/parkings', json={
        'address': parking.address,
        'opened': parking.opened,
        'count_places': parking.count_places,
        'count_available_places': parking.count_available_places
    })
    assert response.status_code == 201
