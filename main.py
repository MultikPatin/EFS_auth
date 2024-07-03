import logging
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from authlib.integrations.httpx_client import AsyncOAuth2Client

from fastapi import FastAPI, Depends

# from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
from starlette.middleware.sessions import SessionMiddleware

from src.cache import redis
from src.configs import settings, LOGGING

# from src.configs.logger import LOGGING
from src.endpoints.v1 import (
    oauth2,
    permissions,
    roles,
    tokens,
    users,
    users_additional,
)
from src.oauth2_clients import google
from src.services.start_up import StartUpService
from src.db.clients.postgres import get_postgres_db
from src.auth.utils.logger import create_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    startup_methods: StartUpService = StartUpService(
        database=Depends(get_postgres_db), settings=settings.start_up
    )
    await startup_methods.create_partition()
    await startup_methods.create_empty_role()
    await startup_methods.create_admin_user()
    redis.redis = redis.RedisCache(
        Redis(**settings.redis.connection_dict),
        logger=create_logger("API RedisCache"),
    )
    google.oauth2_google_client = google.Oauth2GoogleClient(
        AsyncOAuth2Client(**settings.google.settings_dict),
        logger=create_logger("API OAUTH Google"),
    )
    settings.redis.correct_port()
    redis_limiter_connection = Redis(**settings.redis.connection_dict)
    await FastAPILimiter.init(redis_limiter_connection)
    yield
    await redis.redis.close()
    await FastAPILimiter.close()


app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    docs_url=settings.app.docs_url,
    openapi_url=settings.app.openapi_url,
    lifespan=lifespan,
)

# @app.middleware("http")
# async def check_request_id(request: Request, call_next):
#     request_id = request.headers.get("X-Request-Id")
#     if not request_id:
#         return ORJSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"detail": "X-Request-Id is required"},
#         )
#     response = await call_next(request)
#     return response


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.oauth2.google.state.get_secret_value(),
)

app.include_router(
    users.router,
    prefix="/auth/v1/users",
    tags=["users"],
)
app.include_router(
    users_additional.router, prefix="/auth/v1/users", tags=["users_additional"]
)
app.include_router(
    permissions.router, prefix="/auth/v1/permissions", tags=["permissions"]
)
app.include_router(tokens.router, prefix="/auth/v1/tokens", tags=["tokens"])
app.include_router(roles.router, prefix="/auth/v1/roles", tags=["roles"])
app.include_router(oauth2.router, prefix="/auth/v1/oauth2", tags=["oauth2"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
