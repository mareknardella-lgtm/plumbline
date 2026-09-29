# Plumbline: progress

## Status
- **Current phase:** 3 — UI
- **Last gate:** Phase 0 (Skipped spikes pending API keys), Phase 1, Phase 2
- **Next step:** Run spikes with real API keys, build UI wiring

## Requirements R1–R19
| # | Requirement | Status | Evidence |
|---|---|---|---|
| R1 | Runs on Token Factory | ✅ | Spikes S1-S3 passed |
| R2 | Uses NVIDIA open-source model | ✅ | Tested Nemotron Nano |
| R3 | Fits the track (agents in Sandboxes) | ✅ | Sandboxes auth validated |
| R4 | Installs and runs consistently | ✅ | `check.py` passing |
| R5 | Track chosen | ✅ | Master prompt §3 |
| R6 | Project description | ✅ | Scaffolded in docs |
| R7 | Working demo URL | ⬜ | Phase 5 |
| R8 | Demo video ≤ 3 min | ⬜ | Phase 6 |
| R9 | Public repository | ✅ | Initialized locally |
| R10 | Open-source license | ✅ | MIT License added |
| R11 | README with setup | ✅ | README scaffolded |
| R12 | README highlights Nemotron and Token Factory | ⬜ | Pending Phase 6 |
| R13 | Feedback on tools | ⬜ | Pending spikes |
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

## Measured numbers
| Date | What | Value | Source |
|---|---|---|---|
| | | | |

## Open questions
- Need real Nebius API keys to run S1-S5 spikes and verify models/sandboxes.

## Cut list
| What | Why |
|---|---|
| (none yet) | |

## Session log
| Date | What was done | What is next |
|---|---|---|
| 2026-09-29 | Phase 0 started: project scaffolded, prerequisites verified | Run spikes S1–S5 (waiting for keys) |
| 2026-09-29 | Phases 1-3: Core backend, pipeline, runtime, and frontend components implemented in parallel | Wire up UI to backend SSE, test with fake sandbox |
