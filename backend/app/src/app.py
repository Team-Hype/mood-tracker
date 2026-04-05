__all__ = ["app"]

import logging
from fastapi import FastAPI

from .common.logging import logging_settings, setup_logging


from .docs import project_docs
from .settings import settings
from .lifespan import lifespan

app = FastAPI(
    **project_docs.specification,
    lifespan=lifespan,
    docs_url=settings.SWAGGER_PATH,
    redoc_url=settings.REDOC_PATH,
)

logger = setup_logging()

if logging_settings.ENABLE_SQLALCHEMY_LOGGING:
    logger.warning("Enable sqlalchemy logging")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
