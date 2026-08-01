# server.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    print("Received:", request.form)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)