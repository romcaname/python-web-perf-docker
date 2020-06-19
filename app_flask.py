import flask
import json
import sync_db

app = flask.Flask("python-web-perf")

pool = None


@app.route("/test")
def test():
    a, b = sync_db.get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})


@app.route("/external-test")
def external_test():
    import requests
    requests.get('http://external_service:8001/test/2')
    requests.get('http://external_service:8001/test/0.5')
    return {'ok': 'ok'}

@app.route("/external-db-test")
def external_db_test():
    import requests
    requests.get('http://external_service:8001/test/1')
    a, b = sync_db.write_row()
    a, b = sync_db.get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})
