import logging
from http import HTTPStatus

import uvicorn
from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from httpx import RequestError

from api.v1 import room, viewing
from core.config import app_config
from core.logger import LOGGING
from db.models import Room
from db.mongo_db import init_db

load_dotenv()

app = FastAPI(
    title=app_config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(viewing.router, prefix='/api/v1/viewing', tags=['viewing'])
app.include_router(room.router, prefix='/api/v1/room', tags=['room'])


@app.on_event('startup')
async def startup():
    db = init_db()
    await init_beanie(database=db, document_models=[Room])  # type: ignore


@app.exception_handler(RequestError)
async def bad_storage_request_exception_handler(request, exc):
    http_exc = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.error)
    return await http_exception_handler(request, http_exc)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_config.host,
        port=app_config.port,
        log_config=LOGGING,
        log_level=logging.DEBUG if app_config.is_debug else logging.INFO,
    )
