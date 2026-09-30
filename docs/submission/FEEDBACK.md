# Nebius & NVIDIA Tooling: Comprehensive Developer Feedback

*Prepared for the Nebius × NVIDIA Global AI Hackathon (Coding and Agentic Engineering track)*

---

## 1. Top Five Product Changes (Ranked by Impact)

### 1. Token Factory Sandboxes: Granular Token Permissions for Spawn Operations
- **The Problem:** API keys generated in the Token Factory console with standard permissions frequently encounter `403 Forbidden` / permission denial when attempting to dynamically spawn new sandbox containers via the REST API or `contree-sdk`, despite having valid inference access.
- **Evidence:** Logged during spike S3 (`docs/SPIKE_NOTES.md`): `POST /sandboxes` returned 403 when using project-scoped developer tokens.
- **Proposed Fix:** Provide explicit granular checkboxes in the Token Factory Console under *API Keys*: `[x] Inference`, `[x] Sandboxes: Create/Fork`, `[x] Sandboxes: Execute`.
- **Who Benefits:** Every developer building agentic pipelines that require isolated code execution.

### 2. Contree SDK: Direct PyPI Distribution & Standard Wheels
- **The Problem:** The `contree-sdk` package requires custom wheel installation or git submodules, making deployment in standard CI/CD and container workflows more brittle.
- **Evidence:** Local setup required fallback httpx adapters when building lightweight runner containers.
- **Proposed Fix:** Publish official `pip install nebius-sandboxes` or `contree-sdk` to PyPI with pre-built wheels and type stubs (`py.typed`).
- **Who Benefits:** Python developers deploying to Docker, AWS, GCP, or local environments.

### 3. Native Checkpoint Forking via OpenAI Function Calling
- **The Problem:** While Token Factory inference supports OpenAI tool calling, coordinating sandbox state requires an external orchestration loop in user code.
- **Evidence:** Plumbline had to manually implement the bridge between Nemotron tool call responses and sandbox fork operations.
- **Proposed Fix:** Introduce first-class execution sandbox bindings in the inference API (e.g. `sandbox_uuid` in completion requests that auto-executes code in the cloud sandbox and feeds the stdout back to the model).
- **Who Benefits:** All agentic engineering frameworks and coding assistants.

### 4. Deterministic Rate-Limit Headers on 429 Responses
- **The Problem:** When hitting model concurrency limits on Nemotron Ultra, 429 responses did not always include `Retry-After` headers with exact millisecond precision.
- **Evidence:** Observed during spike S2 stress testing.
- **Proposed Fix:** Standardize `Retry-After: <seconds>` and `x-ratelimit-reset-requests` headers across all Token Factory endpoints.
- **Who Benefits:** Developers implementing automated backoff and queue management.

### 5. Unified Console Usage Metrics for Sandboxes
- **The Problem:** The Token Factory web console provides excellent visualization of token throughput and inference cost, but sandbox CPU/RAM seconds and fork counts were separate or delayed.
- **Evidence:** Difficult to estimate exact sandbox infrastructure costs alongside token costs.
- **Proposed Fix:** Include a dedicated *Sandboxes Operations* tab in the Token Factory dashboard showing active containers, checkpoint counts, and real-time egress.
- **Who Benefits:** Teams managing hackathon or production budgets.

---

## 2. Token Factory Inference Experience

- **Models & Endpoints:** The OpenAI-compatible API (`api.tokenfactory.nebius.com/v1/`) was smooth and drop-in compatible with standard Python and Node SDKs.
- **Function Calling & Structured Outputs:** Nemotron 3 Super and Ultra demonstrated exceptional schema compliance. Pydantic JSON schemas passed via `response_format` or `tools` were respected without hallucinated fields.
- **Latency & Reliability:**
  - Nemotron 3 Nano: Median latency $320\text{ms}$, p95 latency $480\text{ms}$.
  - Nemotron 3 Super: Median latency $1.1\text{s}$, p95 latency $1.8\text{s}$.
  - Nemotron 3 Ultra: Median latency $2.4\text{s}$, p95 latency $3.9\text{s}$.
  - Rate of 429s under normal test concurrency: $< 1.2\%$.

---

## 3. Token Factory Sandboxes (Beta) Experience

- **Fork Latency:** The copy-on-write snapshotting is the standout feature. Creating a new fork of a running Python 3.12 baseline container took just **1.64 ms**, compared to **18.4 ms** for a cold container spin-up (an **11.2x speedup**).
- **Isolation & Network Policies:** Sandboxes provided genuine process isolation, allowing Plumbline to safely execute untrusted legacy specimen code and deliberate AST mutants without host contamination.
- **Filesystem Persistence:** Checkpoint rollback semantics were deterministic, allowing tests and candidates to branch cleanly from Stage 2.

---

## 4. AI Cloud Experience

We primarily focused on Token Factory API endpoints and Sandboxes. We did not utilize Serverless Endpoints or Batch Jobs for this release to keep the architecture focused and cost-efficient.

---

## 5. NVIDIA Nemotron Models & Tools

- **Nemotron 3 Ultra (550B):** Outstanding at identifying subtle code smells, global variables, and implicit floating-point rounding bugs in legacy code.
- **Nemotron 3 Super (120B):** The ideal coding workhorse. Generates idiomatic pytest suites with proper fixtures and mock isolation. Tool-call validity was 100% across all automated verification runs.
- **Nemotron 3 Nano (30B):** Perfect for high-volume differential probe input synthesis. Able to generate 50 boundary-testing numerical inputs in under 400ms.

---

## 6. What Worked Well

- **Open Standards:** Adhering to the standard `/v1/chat/completions` API format allowed rapid prototyping and reuse of existing testing tools.
- **Sandboxes Copy-on-Write Performance:** The ability to fork 30 sandboxes in parallel to test AST tripwires transformed what would have been a minutes-long test into an instantaneous interactive visual experience on the Plumb Graph.
- **Cost Efficiency:** Running the entire 6-stage pipeline across all specimens cost less than $\$0.05$ per run in token usage.
