import quart
import json
from async_db import get_row

app = quart.Quart("python-web-perf")

pool = None

@app.route("/test")
async def test():
    a, b = await get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})
