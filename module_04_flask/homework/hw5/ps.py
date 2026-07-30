"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

import html
import subprocess

from flask import Flask
from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps():
    ps_list = request.args.getlist('arg', type=str)
    if not ps_list:
        return "<pre>No arguments provided</pre>", 400
    combined_args = ''.join(ps_list)
    result = subprocess.run(['ps', combined_args], capture_output=True, text=True)
    output = result.stdout
    if result.stderr:
        output += "\n" + result.stderr
    escaped_output = html.escape(output)
    return f"<pre>{escaped_output}</pre>", 200


if __name__ == "__main__":
    app.run(debug=True)
