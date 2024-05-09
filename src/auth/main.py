import logging
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from authlib.integrations.httpx_client import AsyncOAuth2Client
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from redis.asyncio import Redis
from starlette.middleware.sessions import SessionMiddleware

from src.auth.cache import redis
from src.auth.core.config import settings
from src.auth.core.logger import LOGGING
from src.auth.endpoints.v1 import (
    oauth2,
    permissions,
    roles,
    tokens,
    users,
    users_additional,
)
from src.auth.oauth_clients import google
from src.auth.utils.startup import StartUpService
from src.core.configs.postgres import PostgresAuthSettings
from src.core.db.clients.postgres import PostgresDatabase
from src.core.utils.logger import create_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    startup_methods: StartUpService = StartUpService(
        PostgresDatabase(PostgresAuthSettings()),
    )
    await startup_methods.create_empty_role()
    await startup_methods.create_admin_user()
    redis.redis = redis.RedisCache(
        Redis(**settings.redis.connection_dict),
        logger=create_logger("API RedisCache"),
    )
    google.google = google.OauthGoogle(
        AsyncOAuth2Client(**settings.google.settings_dict),
        logger=create_logger("API OAUTH Google"),
    )
    yield
    await redis.redis.close()


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name="localhost",
                agent_port=6831,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )


configure_tracer()
app = FastAPI(
    title=settings.name,
    description=settings.description,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    lifespan=lifespan,
)
FastAPIInstrumentor.instrument_app(app)


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
    secret_key=settings.google.google_state.get_secret_value(),
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
        host=settings.host,
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
