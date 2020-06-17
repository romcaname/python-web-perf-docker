from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from async_db import get_row


async def homepage(request):
    a, b = await get_row()
    return JSONResponse({"a": str(a).zfill(10), "b": b})


routes = [
    Route("/test", endpoint=homepage)
]


app = Starlette(routes=routes)
