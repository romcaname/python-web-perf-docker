from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import async_db

import logging

logger = logging.getLogger()
logger.setLevel('CRITICAL')


async def homepage(request):
    a, b = await async_db.emulate_long_running_query()
    return JSONResponse({"a": str(a).zfill(10), "b": b})

async def long_query_test(request):
    a, b = await async_db.emulate_long_running_query()
    return JSONResponse({"a": str(a).zfill(10), "b": b})


routes = [
    Route("/test", endpoint=homepage),
    Route("/long-query-test", endpoint=long_query_test)
]

app = Starlette(routes=routes)
