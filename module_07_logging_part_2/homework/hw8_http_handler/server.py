from flask import Flask, request, jsonify

app = Flask(__name__)
logs = []  # хранилище логов (в памяти)

@app.route('/log', methods=['POST'])
def add_log():
    """Принимает лог от HTTPHandler и сохраняет его."""
    log_data = request.form.to_dict()  # или просто request.form
    logs.append(log_data)
    print("Received log:", log_data)
    return 'OK', 200

@app.route('/log', methods=['GET'])
def get_logs():
    """Возвращает все сохранённые логи в формате JSON."""
    return jsonify(logs), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)