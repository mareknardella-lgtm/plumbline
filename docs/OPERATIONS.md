# Plumbline: Operations and Credit Management Manual

This guide describes the operational procedures, credit consumption strategy, rate limiting, and emergency procedures for running Plumbline throughout the Nebius × NVIDIA Global AI Hackathon judging period (until 15 Dec 2026).

---

## 1. Credit Burn & Budget Management

Plumbline operates under strict budget guards configured in `.env` and managed by `backend/app/budget/guard.py`.

### Budget Caps
- **Daily Spend Cap:** `$0.50` (`DAILY_BUDGET_USD`)
- **Quick Run Limit:** `$0.60` (`RUN_BUDGET_USD_QUICK`)
- **Thorough Run Limit:** `$1.50` (`RUN_BUDGET_USD_THOROUGH`)
- **Per-IP Rate Limit:** 3 live runs per hour per IP (`LIVE_RUNS_PER_IP_PER_HOUR`)
- **Maximum Concurrent Runs:** 2 (`MAX_CONCURRENT_RUNS`)
- **Maximum Sandbox Concurrency:** 30 parallel forks (`MAX_SANDBOX_CONCURRENCY`)

### Graceful Replay-Only Fallback
If the daily spend limit is reached or if API keys are not supplied:
1. The backend automatically switches to `REPLAY_ONLY=true`.
2. The UI displays an amber status pill: **Replay Mode • Token Factory Sandboxes**.
3. All three recorded runs (`invoice_totals`, `log_digester`, `schedule_builder`) stream in full high-fidelity with adjustable speeds ($1\times, 2\times, 4\times$) and zero Token Factory inference spend.
4. Once the daily quota resets at 00:00 UTC, live runs automatically resume.

---

## 2. Emergency Kill Switch

To immediately pause all live agent and sandbox operations:

1. **Option A: Environment Variable**
   Set `REPLAY_ONLY=true` in `.env` and restart the service:
   ```bash
   # In .env
   REPLAY_ONLY=true
   ```

2. **Option B: Daily Budget Zero**
   Set `DAILY_BUDGET_USD=0.00` to immediately block new inference requests.

3. **Option C: Process Stop**
   ```powershell
   # Stop running docker container
   docker compose down
   # Or terminate local uvicorn process
   Get-Process uvicorn | Stop-Process
   ```

---

## 3. Judge Pass Mechanism

For hackathon judges requiring unrestricted live execution during evaluation:
- Pass the token configured in `JUDGE_PASS` via URL parameter:
  `https://<deployment-url>/?judge_pass=<secret_token>`
- The budget guard bypasses the per-IP hourly rate limit for authenticated judge sessions and allocates a dedicated budget of `$2.00` from `JUDGE_DAILY_BUDGET_USD`.

---

## 4. Uptime Monitoring

Configure an uptime check (e.g. Better Uptime, UptimeRobot, or GitHub Actions workflow) pointing to:
- **Healthcheck URL:** `GET https://<deployment-url>/api/health`
- **Expected Status:** `200 OK`
- **Expected JSON Payload:**
  ```json
  {
    "status": "ok",
    "replay_only": false,
    "version": "1.0.0"
  }
  ```
- **Interval:** 60 seconds
- **Alert Channel:** Email / Slack notification on failure.

---

## 5. Log Inspection and Diagnostics

### Unified Docker Logs
```bash
docker compose logs -f --tail=100
```

### Local Database and Event Inspection
All runs, stages, and emitted events are stored in the SQLite database (`data/plumbline.db`):
```bash
uv run python -c "import sqlite3; db=sqlite3.connect('data/plumbline.db'); print('Total runs:', db.execute('SELECT count(*) FROM runs').fetchone()[0])"
```

### Generated Artifacts
Dossiers, diff patches, and evidence files are saved under `data/runs/<run_id>/`:
- `evidence.json`: Complete quantitative evidence matrix.
- `refactor.patch`: Unified diff patch.
- `dossier.md`: Human-readable markdown audit.
