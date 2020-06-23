import random
import aiopg
import string

pool = None

import asyncpg


async def get_pool():
    global pool
    if pool is None:
        pool = await aiopg.create_pool(
            maxsize=40,
            dsn="dbname=test user=test password=test port=5432 host=db"
        )
    return pool


max_n = 1000_000 - 1


async def get_row():
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            index = random.randint(1, max_n)
            await cursor.execute("select a, b from test where a = %s", (index,))
            ((a, b),) = await cursor.fetchall()
    return a, b


async def emulate_long_running_query(sleep_time=1):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("select pg_sleep(%s)", (sleep_time,))
            await cursor.fetchall()
    return 'a', 'b'


async def write_row():
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            index = random.randint(1, max_n)
            rng = random.Random(0)
            short_random_string = "".join(rng.choice(string.ascii_letters) for _ in range(20))
            await cursor.execute(
                "insert into test(a, b) values (%s, %s) ON CONFLICT ON CONSTRAINT test_pkey DO UPDATE SET b=excluded.b;",
                (index, short_random_string,))
            ((a, b),) = await cursor.fetchall()

    return a, b


async def get_asyncpg_pool():
    global pool
    if not pool:
        pool = await asyncpg.create_pool(database='test', user='test', password='test', port='5432', host='db')
    return pool


async def asyncpg_get_row():
    pool = await get_asyncpg_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            index = random.randint(1, max_n)
            result = await conn.fetchval("select a, b from test where a = %s", (index,))
    return result


async def asyncpg_emulate_long_running_query(sleep_time=1):
    pool = await get_asyncpg_pool()
    async with pool.acquire() as conn:
        result = await conn.fetchval("select pg_sleep(1)")
    return 'a', 'b'
