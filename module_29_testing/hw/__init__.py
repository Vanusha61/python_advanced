from flask import Flask, jsonify, request
from .model import db
from datetime import datetime


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .model import Client, Parking, ClientParking

    @app.before_request
    def before_request():
        with app.app_context():
            db.create_all()

    @app.teardown_appcontext
    def teardown_appcontext(exception=None):
        db.session.remove()

    @app.route('/clients', methods=['GET'])
    def clients():
        all_clients = db.session.query(Client).all()
        clients_list = [
            {
                'id': c.id,
                'name': c.name,
                'surname': c.surname,
                'credit_card': c.credit_card,
                'car_number': c.car_number
            }
            for c in all_clients
        ]
        return jsonify({'clients': clients_list})

    @app.route('/clients/<int:id>', methods=['GET'])
    def client(id):
        client = db.session.query(Client).filter(Client.id == id).first()
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        return jsonify({
            'id': client.id,
            'name': client.name,
            'surname': client.surname,
            'credit_card': client.credit_card,
            'car_number': client.car_number
        }), 200

    @app.route('/clients', methods=['POST'])
    def created_clients():
        clients_data = request.get_json()
        name = clients_data.get('name')
        surname = clients_data.get('surname')
        credit_card = clients_data.get('credit_card', '')
        car_number = clients_data.get('car_number', '')
        if not name or not surname:
            return jsonify({'error': 'Please provide both name and surname'}), 400
        client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({
            'client': {
                'id': client.id,
                'name': client.name,
                'surname': client.surname,
                'credit_card': client.credit_card,
                'car_number': client.car_number
            }
        }), 201

    @app.route('/parkings', methods=['POST'])
    def created_parkings():
        parking_data = request.get_json()
        address = parking_data.get('address')
        opened = parking_data.get('opened', False)
        count_places = parking_data.get('count_places')
        count_available_places = parking_data.get('count_available_places')
        if not address or not count_places or not count_available_places:
            return jsonify({'error': 'Please provide both address and count_place and count_available_places'}), 400
        parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({
            'parking': {
                'id': parking.id,
                'address': parking.address,
                'opened': parking.opened,
                'count_places': parking.count_places,
                'count_available_places': parking.count_available_places
            }
        }), 201

    @app.route('/client_parkings', methods=['POST'])
    def created_client_parking():
        client_parking_data = request.get_json()
        client_id = client_parking_data.get('client_id')
        parking_id = client_parking_data.get('parking_id')
        time_in = datetime.now()
        time_out = None
        if not client_id or not parking_id:
            return jsonify({'error': 'Please provide both client_id and parking_id'}), 400
        clients = db.session.query(Client).filter(Client.id == client_id).first()
        if not clients:
            return jsonify({'error': 'Client not found'}), 404
        parking = db.session.query(Parking).filter(Parking.id == parking_id).first()
        if not parking:
            return jsonify({'error': 'Parking not found'}), 404
        existing = db.session.query(ClientParking).filter(
            ClientParking.client_id == client_id,
            ClientParking.parking_id == parking_id
        ).first()
        if existing:
            return jsonify({'error': 'Client already parked here'}), 400
        if not parking.opened:
            return jsonify({'error': 'Parking is closed'}), 400
        if parking.count_available_places <= 0:
            return jsonify({'error': 'Count_available_places  places not'}), 400
        parking.count_available_places -= 1
        client_parking = ClientParking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=time_in,
            time_out=time_out
        )
        db.session.add(client_parking)
        db.session.commit()
        return jsonify({
            'client_parking': {
                'id': client_parking.id,
                'client_id': client_parking.client_id,
                'parking_id': client_parking.parking_id,
                'time_in': client_parking.time_in.isoformat() if client_parking.time_in else None,
                'time_out': client_parking.time_out.isoformat() if client_parking.time_out else None
            }
        }), 201

    @app.route('/client_parkings', methods=['DELETE'])
    def delete_client_parking():
        client_parking_data = request.get_json()
        client_id = client_parking_data.get('client_id')
        parking_id = client_parking_data.get('parking_id')
        if not client_id or not parking_id:
            return jsonify({'error': 'Please provide both client_id and parking_id'}), 400
        clients = db.session.query(Client).filter(Client.id == client_id).first()
        if not clients:
            return jsonify({'error': 'Client not found'}), 404
        parking = db.session.query(Parking).filter(Parking.id == parking_id).first()
        if not parking:
            return jsonify({'error': 'Parking not found'}), 404

        client_parking = (
            db.session.query(ClientParking)
            .filter(ClientParking.parking_id == parking_id, ClientParking.client_id == client_id,
                    ClientParking.time_out.is_(None))
            .first())

        if not client_parking:
            return jsonify({'error': 'Client parking not found'}), 404
        if clients.credit_card == '' or clients.credit_card is None:
            return jsonify({'error': 'Client has no credit card'}), 400

        parking.count_available_places += 1
        client_parking.time_out = datetime.now()
        db.session.commit()
        return jsonify({'delete': True}), 200

    return app
