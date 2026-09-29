"""Main FastAPI application."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.api.events_sse import router as events_router
from backend.app.api.health import router as health_router
from backend.app.api.replays import router as replays_router
from backend.app.api.runs import router as runs_router
from backend.app.api.specimens import router as specimens_router
from backend.app.budget.guard import BudgetGuard
from backend.app.events.bus import EventBus
from backend.app.llm.client import LLMClient
from backend.app.llm.registry import registry
from backend.app.replay.engine import ReplayEngine
from backend.app.sandbox.adapter import SandboxAdapter
from backend.app.sandbox.fake import FakeSandbox
from backend.app.settings import get_settings
from backend.app.store.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    # Initialize DB
    await init_db()

    # Initialize components
    app.state.event_bus = EventBus()

    if settings.is_replay_only:
        app.state.sandbox = FakeSandbox()
        app.state.llm_client = None
    else:
        app.state.sandbox = SandboxAdapter()
        app.state.llm_client = LLMClient(
            base_url=settings.token_factory_base_url, api_key=settings.nebius_api_key
        )
        # Discover models
        await registry.discover(app.state.llm_client.client)

    app.state.budget_guard = BudgetGuard()
    app.state.replay_engine = ReplayEngine()

    yield

    # Graceful shutdown (e.g. close clients)
    if hasattr(app.state, "llm_client") and app.state.llm_client:
        await app.state.llm_client.client.close()


app = FastAPI(title="Plumbline", lifespan=lifespan)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# API routes
app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(runs_router, prefix="/api/runs", tags=["runs"])
app.include_router(events_router, prefix="/api/runs", tags=["events"])  # /api/runs/{run_id}/events
app.include_router(replays_router, prefix="/api/replays", tags=["replays"])
app.include_router(specimens_router, prefix="/api/specimens", tags=["specimens"])

# Serve frontend static files if they exist
frontend_dist = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists() and frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
