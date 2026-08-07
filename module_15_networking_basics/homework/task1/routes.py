from flask import Flask, request, jsonify

from model import add_room, add_booking, all_rooms
from module_05_processes_and_threads.homework.hw5_add.self_printing import result

app = Flask(__name__)

@app.route("/add-room", methods=["POST"])
def add_rooms():
    response = request.get_json()
    if not response:
        return jsonify({"message": "No room added"}), 400
    floor = response.get('floor')
    beds = response.get('beds')
    guest_num = response.get('guestNum')
    price = response.get('price')
    room_id = add_room(floor, beds, guest_num, price)
    return jsonify({"room":{"message": "Room added", "room_id": room_id}}), 200

@app.route("/room", methods=["GET"])
def get_rooms():
    check_in = request.args.get('checkIn')
    check_out = request.args.get('checkOut')
    rooms = all_rooms(check_in, check_out)
    result = []
    for row in rooms:
        # row: (id, floor, beds, guest_num, price)
        room = {
            "roomId": row[0],
            "floor": row[1],
            "beds": row[2],
            "guestNum": row[3],
            "price": row[4]
        }
        result.append(room)
    # функция из модели
    return jsonify({"rooms": result})

@app.route('/booking', methods=["POST"])
def booking():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON", "received": request.data.decode()}), 400
    room_id = data.get('roomId')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    booking_dates = data.get('bookingDates')
    check_in = booking_dates.get('checkIn')
    check_out = booking_dates.get('checkOut')

    result = add_booking(room_id, check_in, check_out, first_name, last_name)
    if isinstance(result, str):
        return jsonify({"error": result}), 409
    return jsonify({"message": "Booking created"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
