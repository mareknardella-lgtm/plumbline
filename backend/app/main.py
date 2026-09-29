"""Plumbline FastAPI application."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown."""
    settings = get_settings()
    # TODO: Initialize services (LLM client, sandbox client, store)
    yield
    # TODO: Graceful shutdown (cancel active runs, close connections)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Plumbline",
        description="Refactor old code without changing what it does, and see the evidence.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # API routes
    from backend.app.api.health import router as health_router
    from backend.app.api.runs import router as runs_router
    from backend.app.api.specimens import router as specimens_router
    from backend.app.api.replays import router as replays_router

    app.include_router(health_router, prefix="/api")
    app.include_router(runs_router, prefix="/api")
    app.include_router(specimens_router, prefix="/api")
    app.include_router(replays_router, prefix="/api")

    return app


app = create_app()
