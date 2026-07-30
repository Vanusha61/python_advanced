"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/uptime', methods=['GET'])
def uptime():
    try:
        # uptime -p выводит "up X days, Y hours, Z minutes"
        output = subprocess.check_output(['uptime', '-p'], text=True).strip()
        return jsonify({"uptime": output}), 200
    except Exception:
        return "Error getting uptime", 500

if __name__ == '__main__':
    app.run(debug=True)
