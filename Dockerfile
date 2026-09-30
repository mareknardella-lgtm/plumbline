# syntax=docker/dockerfile:1
# Multi-stage Dockerfile for Plumbline: Unified Frontend & Backend Production Service

# --- Stage 1: Frontend Build ---
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# --- Stage 2: Backend Runtime ---
FROM python:3.12-slim AS runner

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency specifications
COPY pyproject.toml .
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Copy application code and runtime tools
COPY backend/ ./backend/
COPY runtime/ ./runtime/
COPY spikes/ ./spikes/
COPY scripts/ ./scripts/
COPY docs/ ./docs/

# Copy built frontend assets to frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose web port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start unified production server
CMD ["uv", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
