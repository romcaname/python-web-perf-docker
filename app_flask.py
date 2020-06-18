import flask
import json
from sync_db import get_row

app = flask.Flask("python-web-perf")

pool = None


@app.route("/test")
def test():
    a, b = get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})


@app.route("/external-test")
def external_test():
    import requests
    requests.get('http://external_service:8001/test/2')
    requests.get('http://external_service:8001/test/0.5')
    return {'ok': 'ok'}
