# -*- coding: utf-8 -*-

import asyncio

import pydantic
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from starlette import status
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.routers import trainer, analyser


app = FastAPI(redoc_url=None)

"""подключаем все роутеры апи"""
app.include_router(trainer.router)
app.include_router(analyser.router)

WHLITELISTED_IPS = ['127.0.0.1']

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BackgroundRunner:
    """
    чисто служебный класс
    если запускать очередь как обычную функцию то тогда апи нельзя будет нормально убить
    """
    def __init__(self):
        self.value = 0


runner = BackgroundRunner()


@app.exception_handler(pydantic.error_wrappers.ValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "message": 'Unprocessable Entity'}),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    обрабатывает ошибки неправильно формата входящих на апи данных
    возвращает где и что было неправильно
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.on_event("startup")
async def startup():
    """инициализация кеша"""
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    """запустить очередь запросов"""
    # asyncio.get_event_loop().create_task(runner.run_logger())


@app.get("/")
async def read_root(request: Request):
    return status.HTTP_200_OK
