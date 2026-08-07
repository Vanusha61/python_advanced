from flask import Flask, request, jsonify
app = Flask(__name__)


result_list = []
roomId = 0

@app.route("/room", methods=["GET"])
def root():
    available = [r for r in result_list if not r.get("booked", False)]
    return jsonify({"rooms": available})
@app.route("/add-room", methods=["POST"])
def add_room():
    data= request.get_json()
    global roomId
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    new_room = {
        "roomId": roomId,
        "floor": data.get("floor"),
        "beds": data.get("beds"),
        "guestNum": data.get("guestNum"),
        "price": data.get("price"),
        "booked": False
    }
    result_list.append(new_room)
    roomId += 1
    return jsonify({"status": "ok"}), 200

@app.route("/booking", methods=["POST"])
def booking():
    data = request.get_json()
    if data is None or "roomId" not in data:
        return jsonify({"error": "Invalid request"}), 400

    room_id = data["roomId"]
    for r in result_list:
        if r["roomId"] == room_id:
            if r.get("booked", False):
                return jsonify({"error": "Room already booked"}), 409
            r["booked"] = True
            return jsonify({"status": "ok"}), 200
    return jsonify({"error": "Room not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
