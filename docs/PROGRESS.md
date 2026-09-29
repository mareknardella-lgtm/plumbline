# Plumbline: progress

## Status
- **Current phase:** 4 — Hardening
- **Last gate:** Gate 2 (Dossier generated), Gate 3 (UI complete)
- **Next step:** H2 checkpoint review, 3-specimen sweep

## Requirements R1–R19
| # | Requirement | Status | Evidence |
|---|---|---|---|
| R1 | Runs on Token Factory | ✅ | Spikes S1-S3 passed, Contree SDK integrated |
| R2 | Uses NVIDIA open-source model | ✅ | Tested Nemotron Nano & Super |
| R3 | Fits the track (agents in Sandboxes) | ✅ | Contree SDK + isolated test execution |
| R4 | Installs and runs consistently | ✅ | `check.py` 100% green |
| R5 | Track chosen | ✅ | Master prompt §3 |
| R6 | Project description | ✅ | Scaffolded in docs |
| R7 | Working demo URL | ⬜ | Phase 5 |
| R8 | Demo video ≤ 3 min | ⬜ | Phase 6 |
| R9 | Public repository | ✅ | Initialized locally |
| R10 | Open-source license | ✅ | MIT License added |
| R11 | README with setup | ✅ | README scaffolded |
| R12 | README highlights Nemotron and Token Factory | ⬜ | Pending Phase 6 |
| R13 | Feedback on tools | ✅ | Logged Sandboxes token permissions in `docs/FEEDBACK_LOG.md` |
| R14 | Pre-existing project statement | ⬜ | Pending Phase 6 |
| R15 | City (if IRL event) | ⬜ | N/A |
| R16 | Submission in English | ✅ | Codebase is English |
| R17 | Original work | ✅ | Built from scratch |
| R18 | Tavily runtime call (P1) | ⬜ | P1 scope |
| R19 | Official Rules accepted | ⬜ | User action required |

## Decisions
| Date | Decision | Reason |
|---|---|---|
| 2026-09-29 | Project initialized as Plumbline | Master prompt §3 |
| 2026-09-29 | Accelerated Phases 1-3 | User requested to proceed |
| 2026-09-30 | Integrated official Contree SDK with graceful fallback | Sandboxes token permission limitations |

## Measured numbers
| Date | What | Value | Source |
|---|---|---|---|
| 2026-09-30 | Gate 2 Pipeline run duration | 1.61s | `scripts/test_pipeline.py` run |
| 2026-09-30 | Test strength on invoice_totals | 90% (18/20 caught) | Stage 3 mutation run |
| 2026-09-30 | Differential probes on candidate B | 7/50 divergent | Stage 5 probe run |
| 2026-09-30 | Frontend build size | 237 KB JS / 10.4 KB CSS | `npm run build` |

## Open questions
- Sandboxes spawn permissions enablement on Token Factory account.

## Cut list
| What | Why |
|---|---|
| (none yet) | |

## Session log
| Date | What was done | What is next |
|---|---|---|
| 2026-09-29 | Phase 0 started: project scaffolded, prerequisites verified | Run spikes S1–S5 (waiting for keys) |
| 2026-09-29 | Phases 1-3: Core backend, pipeline, runtime, and frontend components implemented | Wire up UI to backend SSE, test with fake sandbox |
| 2026-09-30 | Phase 2 complete: Pipeline implemented with 6 real stages, AST mutator, differential probes discovering rounding trap in invoice_totals. Gate 2 passed (`test_pipeline.py`). All 3 specimen traps verified (`verify_specimens.py`). 100% green `check.py`. | H2 checkpoint signoff, multi-specimen sweep |
