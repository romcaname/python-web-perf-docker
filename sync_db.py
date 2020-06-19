import psycopg2
import psycopg2.pool
import random
import string

pool = None


def get_pool():
    global pool
    if pool is None:
        pool = psycopg2.pool.SimpleConnectionPool(
            1, 4, host='db', database="test", user="test", password="test", port=5432,
        )
    return pool


max_n = 1000_000 - 1


def get_row():
    conn = get_pool().getconn()
    cursor = conn.cursor()
    index = random.randint(1, max_n)
    cursor.execute("select a, b from test where a = %s;", (index,))
    ((a, b),) = cursor.fetchall()
    cursor.close()
    get_pool().putconn(conn)
    return a, b


def write_row():
    conn = get_pool().getconn()
    cursor = conn.cursor()
    index = random.randint(1, max_n)
    rng = random.Random(0)
    short_random_string = "".join(rng.choice(string.ascii_letters) for _ in range(20))
    cursor.execute("insert into test(a, b) values (%s, %s) ON CONFLICT ON CONSTRAINT test_pkey DO UPDATE SET b=excluded.b;",
                   (index, short_random_string,))
    ((a, b),) = cursor.fetchall()
    cursor.close()
    get_pool().putconn(conn)
    return a, b
