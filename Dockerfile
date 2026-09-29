FROM python:3.12-slim AS backend-deps

WORKDIR /app
COPY pyproject.toml uv.lock* ./

RUN pip install uv && uv sync --no-dev --frozen

# Frontend build
FROM node:24-slim AS frontend-build

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --ignore-scripts

COPY frontend/ ./
RUN npm run build

# Final image
FROM python:3.12-slim

WORKDIR /app

# Copy Python deps and app
COPY --from=backend-deps /app/.venv /app/.venv
COPY backend/ backend/
COPY runtime/ runtime/
COPY scripts/ scripts/
COPY docs/ docs/
COPY pyproject.toml README.md LICENSE SECURITY.md THIRD_PARTY.md ./

# Copy built frontend
COPY --from=frontend-build /app/frontend/dist frontend/dist/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
