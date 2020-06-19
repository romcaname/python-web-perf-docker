import aiohttp
import asyncio
import quart
import json
from async_db import get_row, write_row

app = quart.Quart("python-web-perf")

pool = None


@app.route("/test")
async def test():
    a, b = await get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


@app.route("/external-test")
async def external_test():
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(*(fetch(session, i) for i in ['http://external_service:8001/test/2',
                                                                       'http://external_service:8001/test/0.5']))
    return json.dumps({'ok': 'ok'})


@app.route("/external-db-test")
async def external_db_test():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'http://external_service:8001/test/1')
    await write_row()
    a, b = await get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})
