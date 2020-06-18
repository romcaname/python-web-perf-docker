from fastapi import FastAPI
from starlette.responses import JSONResponse

from sync_db import get_row

import logging

logger = logging.getLogger()
logger.setLevel('CRITICAL')

app = FastAPI()


@app.get('/test')
def homepage(request):
    a, b = get_row()
    return JSONResponse({"a": str(a).zfill(10), "b": b})
