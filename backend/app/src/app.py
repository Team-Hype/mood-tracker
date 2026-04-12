__all__ = ["app"]

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .common.logging import logging_settings, setup_logging
from .docs import project_docs
from .lifespan import lifespan
from .routers import router
from .settings import settings

app = FastAPI(
    **project_docs.specification,
    lifespan=lifespan,
    docs_url=settings.SWAGGER_PATH,
    redoc_url=settings.REDOC_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

logger = setup_logging()

if logging_settings.ENABLE_SQLALCHEMY_LOGGING:
    logger.warning("Enable sqlalchemy logging")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
