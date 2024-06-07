from pydantic import BaseModel
from logging.config import dictConfig
import logging


class LogConfig(BaseModel):
    """Logging configuration to be set for the server and gunicorn"""

    LOGGER_NAME: str = "uvicorn.access"
    GUNICORN_LOGGER_NAME: str = "__main__"
    LOG_FORMAT: str = "%(levelprefix)s [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "gunicorn": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
        GUNICORN_LOGGER_NAME: {
            "handlers": ["gunicorn"], "level": LOG_LEVEL
        },
    }


def configure_logging(log_level):
    dictConfig(LogConfig(LOG_LEVEL=log_level).dict())

    gunicorn_logger = logging.getLogger("__main__")
    uvicorn_logger = logging.getLogger("uvicorn.access")
    gunicorn_logger.handlers = uvicorn_logger.handlers
    gunicorn_logger.setLevel(uvicorn_logger.level)
