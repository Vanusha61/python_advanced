import json


def application(environ: dict, start_response):
    path = environ.get('PATH_INFO', '')
    if path.startswith('/hello'):
        user_name = path.split('/')
        start_response('200 OK', [('Content-Type', 'application/json')])
        if len(user_name) == 2 or (len(user_name) == 3 and user_name[2] == ''):
            return [json.dumps({"message": "hello", "name": "username"}).encode('utf-8')]
        elif len(user_name) > 3:
            start_response('400 Bad Request', [('Content-Type', 'application/json')])
            return [json.dumps({"message": "Bad Request"}).encode('utf-8')]
        return [json.dumps({"message": "hello", "name": user_name[2]}).encode('utf-8')]
    start_response('404 Not Found', [('Content-Type', 'application/json')])
    return [json.dumps({"message": "Not Found"}).encode('utf-8')]
