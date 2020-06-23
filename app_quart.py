import aiohttp
import asyncio
import asyncpg
import quart
import json
import async_db

app = quart.Quart("python-web-perf")

pool = None


#only for asyncpg
@app.before_serving
async def startup():
    app.pool = await asyncpg.create_pool(max_size=10, min_size=10, database='test', user='test', password='test', port='5432', host='db')


@app.route("/test")
async def test():
    a, b = await async_db.get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})


@app.route("/long-query-test")
async def long_query_test():
    async with app.pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchval("select pg_sleep(1)")
            a, b = 'a', 'b'
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
    await async_db.write_row()
    a, b = await async_db.get_row()
    return json.dumps({"a": str(a).zfill(10), "b": b})
