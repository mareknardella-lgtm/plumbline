# Plumbline Architecture

Plumbline is an agentic refactoring and verification engine that guarantees behavioral preservation during legacy code modernization.

```
                                      ┌────────────────────────────────────────────────────────┐
                                      │              Plumbline Orchestrator                    │
                                      │  (FastAPI • Event Bus • Token Factory AsyncOpenAI)     │
                                      └──────────────────────────┬─────────────────────────────┘
                                                                 │
      ┌──────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────┐
      │                                                          │                                                          │
┌─────▼──────────────────────────────┐       ┌───────────────────▼──────────────────┐       ┌───────────────────────────────▼─────┐
│       NVIDIA Nemotron Models       │       │    Token Factory Sandboxes (COW)     │       │       Frontend & Telemetry          │
├────────────────────────────────────┤       ├──────────────────────────────────────┤       ├─────────────────────────────────────┤
│ • Ultra 550b: Architectural Survey │       │ • Baseline Checkpoint (Original Code)│       │ • React 19 + TypeScript + Vite      │
│ • Super 120b: Pins & Refactoring   │       │ • Copy-on-Write Forks (1.64ms setup) │       │ • Real-time Plumb Graph (inline SVG)│
│ • Nano 30b: Probes & Triage        │       │ • Parallel Mutants (30 concurrent)   │       │ • SSE Event Reducer (Last-Event-ID) │
│ • Lightning 3.5: Fast Fallback     │       │ • Hermetic Isolation (Network blocked│       │ • Accessible Table & Diff View      │
└────────────────────────────────────┘       └──────────────────────────────────────┘       └─────────────────────────────────────┘
```

---

## 1. System Overview

Plumbline operates on the principle that **unit tests written by a model alone do not prove behavioral preservation**. To prevent subtle regressions (penny rounding, sort ties, mutable defaults, timezone drift), Plumbline combines:
1. **Model Specialization:** Role-based routing across NVIDIA Nemotron 3 tiers (Ultra, Super, Nano).
2. **Copy-on-Write Sandbox Isolation:** Token Factory Sandboxes providing sub-2ms fork latencies for deterministic, isolated executions.
3. **Cryptographic Integrity:** Hash-locking to ensure test suites cannot be weakened or altered during refactoring.
4. **Differential Probing:** Executing candidate code alongside the original on tens of unseen synthetic inputs.
5. **Real-time Geometric Telemetry:** The Plumb Graph displays tensioned lines whose deflection angles directly map to behavioral drift.

---

## 2. Six-Stage Verification Pipeline

```
  Stage 1          Stage 2          Stage 3          Stage 4          Stage 5          Stage 6
 [Survey]   ───▶  [Record]   ───▶  [Mutate]   ───▶  [Refactor] ───▶  [Compare]  ───▶  [Dossier]
 Ultra 550b      Super 120b       AST Mutator      Super / Nano     Nano Probes      Super 120b
AST pre-pass    Pytest pins      Tripwires         Parallel forks   Side-by-side     evidence.json
Effect flags    Coverage gate    Strength >= 85%   Hash-locked src  Drift = 0        refactor.patch
```

### Stage 1: Survey (`stage1_survey.py`)
- **Deterministic Pre-pass:** Parses Python source AST inside a sandbox. Extracts public callables, parameter signatures, imports, and stateful effect flags (`file_io`, `network`, `time`, `randomness`, `globals`, `print`).
- **Architectural Synthesis:** Nemotron 3 Ultra synthesizes a structured `SurveyReport` containing risks, call recipes, and neutralization strategies.

### Stage 2: Record (`stage2_record.py`)
- **Characterization Pins:** Nemotron 3 Super synthesizes pytest characterization tests capturing exact legacy quirks, including edge cases and non-standard returns.
- **Hermetic Test Harness:** Generates a custom `conftest.py` freezing system clock, seeding RNG, fixing locale to UTF-8, and strictly blocking outbound network sockets.
- **Flakiness Verification:** Tests run across distinct execution nonces. Flaky tests are eliminated.
- **Baseline Checkpoint:** Creates a persistent snapshot containing original code, runtime tools, and locked test suite. Line coverage must exceed 70%.

### Stage 3: Plant Bugs / Tripwires (`stage3_mutate.py`)
- **Deterministic Mutator:** Applies 8 distinct AST mutation operators:
  - Comparison swap (`<` ↔ `<=`, `==` ↔ `!=`, `>` ↔ `>=`)
  - Arithmetic swap (`+` ↔ `-`, `*` ↔ `//`)
  - Boolean swap (`and` ↔ `or`)
  - Condition inversion (`if x:` ➔ `if not x:`)
  - Constant shift (`n` ➔ `n ± 1`, `True` ➔ `False`, `""` ➔ `"x"`)
  - Return `None` injection
  - Statement deletion
  - Range / off-by-one alteration
- **Parallel Sandbox Execution:** The baseline checkpoint is forked into 30 parallel sandboxes. Each mutant runs against the locked pins.
- **Test Strength Gate:** Test strength $\ge 85\%$ is required. If strength falls below 85%, Super runs targeted strengthening rounds against surviving mutants. Nemotron Nano triages survivors as equivalent or true gaps.

### Stage 4: Try Refactors (`stage4_refactor.py`)
- **Parallel Candidate Strategies:**
  - **Candidate A (Conservative - Nemotron Nano):** Minimal touch, strict modernization, preserving existing algorithmic structure.
  - **Candidate B (Balanced - Nemotron Super):** Idiomatic refactoring, helper decomposition, type annotations, and standard library cleanups.
  - **Candidate C (Ambitious - Nemotron Ultra):** Structural re-architecture for high maintainability.
- **Hash Guard:** Any modification outside `src/` is rejected cryptographically. Tests cannot be modified to force a pass.
- **Anti-Cheating:** Checks prevent hardcoding test input literals into refactored sources.

### Stage 5: Compare (`stage5_compare.py`)
- **Differential Probing:** Nemotron Nano synthesizes diverse, unseen numerical and state inputs.
- **Side-by-Side Execution:** The original baseline and candidate fork execute each probe under identical sandboxed conditions.
- **Drift Calculation:**
  - $0$ drift: All outputs match original byte-for-byte.
  - $>0$ drift: Pinpoints the exact input and divergence delta.
- **Verdict Determination:** A candidate receives **HOLDS TRUE** only if locked pins pass (100%), no probes diverge, and the API signature remains identical.

### Stage 6: Dossier (`stage6_dossier.py`)
- **Deterministic Assembly:** Collates all test metrics, coverage percentages, tripwire results, probe results, and git diffs into `evidence.json`.
- **Narrative Generation:** Nemotron Super authors `dossier.md` using numbers strictly verified against `evidence.json`.
- **Artifacts:** Produces `evidence.json`, `refactor.patch`, `pins.zip`, and `pr_description.md`. Concludes with an explicit *"What this does not prove"* boundary statement.

---

## 3. Token Factory Sandboxes Fork Tree

```
                           [Root Image: Python 3.12 hermetic]
                                           │
                                           ▼
                            [Baseline Checkpoint UUID]
                     (Original Code + conftest.py + Locked Pins)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
   [Mutant Forks]                  [Candidate Forks]                 [Probe Side-by-Side]
   Fork 1 .. Fork 30               Fork A (Conservative)            Baseline vs Candidate
   (Run AST tripwires)             Fork B (Balanced)                (Execute 50 unseen inputs)
   1.64ms setup time               Fork C (Ambitious)               Bitwise output comparison
```

- **Cold Environment Setup:** 18.4 ms
- **Copy-on-Write Sandbox Fork:** 1.64 ms (**11.2x speedup**)
- **Concurrency:** Up to 30 parallel forks running concurrently during Stage 3.

---

## 4. Frontend & Geometric Layout

The Plumb Graph is rendered as a custom, responsive inline SVG (`frontend/src/graph/PlumbGraph.tsx`):
- **Anchor & Plumb Line:** A tensioned vertical line (`--plumb`) anchored at the top center.
- **Checkpoints:** Visual nodes at Stage 2 (Recording baseline) and Stage 3 (Tripwires).
- **Mutant Tick Strip:** A horizontal density strip showing caught, survived, and timed-out mutations.
- **Candidate Cables & Bobs:** Cables hang from the baseline. Lateral angular deflection ($\theta = \text{clamp}(\text{drift} \times 30^\circ, 0^\circ, 30^\circ)$) visualizes divergence.
- **Verdict Settle:** Winner settles with a damped spring animation (700-900ms), respecting `prefers-reduced-motion`.
- **Accessibility:** Accessible table alternative (`PlumbGraphTable.tsx`) provides 100% feature parity for screen-readers.
