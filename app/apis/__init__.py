from . import health, user
from fastapi import FastAPI
from app.config import config


def configure_routes(app: FastAPI):
    app.include_router(router=health.router, prefix=config.OPENAPI_PREFIX)
    app.include_router(router=user.router, prefix=config.OPENAPI_PREFIX)
