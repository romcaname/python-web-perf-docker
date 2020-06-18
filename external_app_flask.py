import flask
import json
app = flask.Flask("python-external-service")


@app.route("/test/<sleep_time>")
def test(sleep_time):
    import time
    time.sleep(float(sleep_time))
    return json.dumps({'ok': 'ok'})
