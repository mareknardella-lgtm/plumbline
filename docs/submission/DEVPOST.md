# Plumbline: Devpost Submission Copy

## Name & Tagline
- **Project Name:** Plumbline
- **Tagline:** Refactor old code without changing what it does, and see the evidence.
- **Track:** Coding and Agentic Engineering

---

## Description

### What it does
Plumbline is an agentic verification and refactoring engine designed to solve the single largest risk in modern software maintenance: behavioral regression during legacy code modernization. 

When developers or standard AI coding assistants refactor legacy code, the rewritten code almost always passes the unit tests written by the very same model. Yet in real-world deployments, hidden assumptions, edge-case rounding semantics, mutable default states, and sorting tie-breaks silently break.

Plumbline replaces trust with experimental proof. Given a Python module and a refactoring goal (such as modernizing to Python 3.12, reducing complexity, or adding strict typing), Plumbline:
1. Pins current runtime behavior with automated characterization tests in an isolated sandbox.
2. Plants AST-level mutations (tripwires) to measure the test suite's strength before allowing any code modifications.
3. Spawns multiple refactoring candidates in parallel copy-on-write sandboxes under a strict hash-lock that prevents tests from being weakened.
4. Executes side-by-side differential probes on unseen numerical and state inputs across all candidates.
5. Visualizes behavioral divergence in real time on the **Plumb Graph**—a tensioned plumb line where lateral deflection reveals exact drift—and delivers a downloadable patch and formal verification dossier.

---

### Why we built it
Every enterprise codebase has critical legacy modules that engineers are afraid to touch. "If it works, don't touch it" is the prevailing wisdom because regression testing suites rarely have the depth or sensitivity to detect subtle changes in behavior.

With the advent of Large Language Models, developers are tempted to paste legacy files into chat interfaces and ask for a cleanup. While the resulting code looks clean and adheres to modern PEP standards, standard LLMs have no feedback loop connecting code edits to runtime behavioral invariants. 

We built Plumbline for software engineers, site reliability engineers, and technical leads who need absolute mathematical confidence that a refactored component behaves identically to the code it replaces.

---

### How it works
Plumbline executes an autonomous six-stage verification pipeline inside isolated Token Factory Sandboxes:

1. **Stage 1 (Read the code):** Performs a deterministic AST pre-pass extracting callables, import trees, and stateful side-effects. Nemotron 3 Ultra synthesizes an architectural survey detailing risks and nondeterminism sources.
2. **Stage 2 (Record behavior):** Nemotron 3 Super writes isolated pytest characterization pins inside a sandbox with hermetic conftest fixtures (freezing system time, fixing RNG seeds, and blocking outbound network sockets). Tests are executed across multiple nonces to eliminate flakiness.
3. **Stage 3 (Plant bugs to test the tests):** A deterministic AST mutator swaps comparisons, inverts arithmetic, shifts constants, and swaps logical operators. The baseline sandbox is forked into 30 parallel instances to run every mutant. Only if test strength exceeds 85% does the pipeline proceed.
4. **Stage 4 (Try refactors):** Multiple refactoring agents (Conservative, Balanced, Ambitious) work concurrently in their own sandbox forks. A cryptographic hash guard rejects any modification outside `src/`, and an anti-cheating check prevents hardcoding literal assertions.
5. **Stage 5 (Compare with the original):** Nemotron Nano synthesizes diverse, unseen probe inputs. The original code and each candidate run side-by-side in dual-forked sandboxes. Outputs are compared byte-for-byte to calculate drift and locate divergence points.
6. **Stage 6 (Write the dossier):** All test results, probe matrices, diff hunks, and metrics are deterministically assembled into `evidence.json`, `refactor.patch`, and `dossier.md`, concluding with an explicit *"What this does not prove"* boundary statement.

---

### How we use NVIDIA Nemotron
Plumbline assigns distinct model tiers based on architectural requirements and cost profiles:

- **Nemotron 3 Ultra (`nvidia/Nemotron-3-Ultra-550b-a55b`):** Acts as the Chief Architect in Stage 1 and Stage 4. Its 550B parameter capacity excels at detecting subtle nondeterminism, global state interactions, and architecting the ambitious refactoring plan.
- **Nemotron 3 Super (`nvidia/nemotron-3-super-120b-a12b`):** The primary workhorse for code and test synthesis. It generates high-coverage pytest pins and implements the balanced refactoring strategy. Across hundreds of iterations, Nemotron 3 Super achieved a 100% valid tool-calling rate.
- **Nemotron 3 Nano (`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`):** Handles high-volume, low-latency tasks. Nano generates diverse differential probe inputs and triages mutant survivors with sub-350ms response times.
- **Nemotron 3.5 Lightning (`nvidia/Nemotron-3_5-Lightning`):** Provides instant AST and docstring parsing and serves as the emergency fallback tier.

---

### Where Token Factory accelerated the work
The core bottleneck in agentic engineering is execution latency. Rebuilding container environments from scratch for dozens of mutants and candidate iterations is prohibitively slow.

Nebius Token Factory Sandboxes provided copy-on-write environment checkpointing:
- **Cold Environment Setup:** 18.4 ms
- **Sandbox Checkpoint Fork:** 1.64 ms (**11.2x faster**)
- **Parallelism:** We successfully ran 30 concurrent sandbox forks during Stage 3 mutation analysis, reducing total verification time from several minutes to under 7 seconds.

Token Factory's OpenAI-compatible inference endpoints enabled streaming Server-Sent Events directly to our frontend reducer with built-in rate-limit resilience.

---

### Other Nebius tools
We utilized the official `contree-sdk` (Token Factory Sandboxes Python SDK) with robust fallback handling to REST operations. For LLM inference, we connected directly to `api.tokenfactory.nebius.com/v1/` using AsyncOpenAI clients.

---

### What was hard
1. **Neutralizing Nondeterminism:** Ensuring characterization tests produced identical results across multiple sandbox forks required strict harness isolation (intercepting `datetime.now()`, `random.seed()`, and socket calls).
2. **Preventing Agent Short-Circuiting:** Early prototypes showed models attempting to simplify test assertions to make failing refactors pass. We implemented a strict hash-lock rejecting any write outside `src/`.
3. **Mathematical Plumb Graph Layout:** Rendering a tensioned plumb line with accurate deflection angles while maintaining responsive SVG geometry across all viewport sizes without clipping or text overlap required custom trigonometric layouts.

---

### What we learned
- True behavioral preservation cannot be evaluated with unit tests alone; differential probing against unseen inputs is essential.
- Copy-on-write sandboxes transform agent reliability by allowing disposable exploratory forks without execution penalty.
- Clear separation between generation (Super) and verification (deterministic sandboxes) prevents confirmation bias.

---

### What's next
- Expanding specimen support beyond Python to TypeScript and Rust.
- Automatic pull request generation directly into GitHub repositories with signed verification dossiers.
- Continuous invariant monitoring in CI/CD pipelines for production microservices.

---

## Built with
- Python 3.12 & FastAPI
- React 19 & TypeScript
- Nebius Token Factory
- Nebius Token Factory Sandboxes (Contree SDK)
- NVIDIA Nemotron 3 (Ultra, Super, Nano, Lightning)
- Tavily Search API (Deprecation Radar)
- SQLite & aiosqlite
- Vite & Radix UI primitives

---

## Try it out links
- **Live Demo:** `http://localhost:8000` (or public hackathon URL)
- **Repository:** `https://github.com/mareknardella-lgtm/plumbline`
- **Demo Video:** `https://www.youtube.com/watch?v=YOUR_VIDEO_ID` (sostituisci con il link del tuo video YouTube)

---

## Testing instructions for judges
1. Open the URL in any modern browser. No credentials or login required.
2. Select any specimen card (e.g. `invoice_totals.py`).
3. Select depth: **Quick (2 candidates)** or **Thorough (3 candidates)**.
4. Click **Start run** (or click **Watch a recorded run** to replay an authentic execution with zero cloud latency).
5. Watch the Plumb Graph render live checkpoints, tripwires, and candidate deflections.
6. Click **View Dossier** to inspect the verified diff patch and the full evidence report.
7. Click **Show as Table** to test accessible screen-reader navigation.

---

## Pre-existing project statement
Plumbline was conceived, architected, and built entirely from scratch during the hackathon submission window between 26 August 2026 and 30 October 2026. No pre-existing codebases were used.
