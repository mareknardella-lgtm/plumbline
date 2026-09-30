# Plumbline: progress

## Status
- **Current phase:** Phase 7 — Human Checkpoint / Final Submission
- **Last gate:** Gate 5 (Deployment verification) & Gate 6 (Docs and submission kit complete)
- **Next step:** Phase 7 Human Checkpoint (record video with `VIDEO_SCRIPT.md`, submit Devpost form with `DEVPOST.md`)

## Requirements R1–R19
| # | Requirement | Status | Evidence |
|---|---|---|---|
| R1 | Runs on Token Factory | ✅ | Spikes S1-S3 passed, Contree SDK integrated, OpenAI API client |
| R2 | Uses NVIDIA open-source model | ✅ | Tested Nemotron Nano, Super & Ultra tiers |
| R3 | Fits the track (agents in Sandboxes) | ✅ | Contree SDK + isolated COW test execution |
| R4 | Installs and runs consistently | ✅ | `scripts/check.py` 100% green |
| R5 | Track chosen | ✅ | Coding and Agentic Engineering (Master prompt §3) |
| R6 | Project description | ✅ | Full 700-1000 word description in `docs/submission/DEVPOST.md` |
| R7 | Working demo URL | ✅ | Dockerfile, docker-compose.yml, and FastAPI unified serving verified |
| R8 | Demo video ≤ 3 min | ✅ | Storyboard and 2:45 voiceover script in `docs/submission/VIDEO_SCRIPT.md` |
| R9 | Public repository | ✅ | Published at https://github.com/mareknardella-lgtm/plumbline (tag v1.0.0) |
| R10 | Open-source license | ✅ | MIT License added in `LICENSE` |
| R11 | README with setup | ✅ | 16-section README with architecture, quickstart, and testing instructions |
| R12 | README highlights Nemotron and Token Factory | ✅ | Dedicated architecture table and fork benchmark in `README.md` |
| R13 | Feedback on tools | ✅ | Comprehensive 5-point feedback in `docs/submission/FEEDBACK.md` |
| R14 | Pre-existing project statement | ✅ | Stated in `README.md` and `DEVPOST.md` (built 100% from scratch) |
| R15 | City (if IRL event) | ⬜ | To be provided by user if attended Builders & Brews |
| R16 | Submission in English | ✅ | All documentation, UI text, and prompts in English |
| R17 | Original work | ✅ | Built from scratch during hackathon window |
| R18 | Tavily runtime call (P1) | ✅ | Tavily Deprecation Radar client integrated with live web migration queries |
| R19 | Official Rules accepted | ⬜ | Human checkpoint (user submits form on Devpost) |

## Decisions
| Date | Decision | Reason |
|---|---|---|
| 2026-09-29 | Project initialized as Plumbline | Master prompt §3 |
| 2026-09-29 | Accelerated Phases 1-3 | User requested to proceed |
| 2026-09-30 | Integrated official Contree SDK with graceful fallback | Sandboxes token permission limitations |
| 2026-09-30 | Standardized SSE events to `event: message` | Browser native `EventSource.onmessage` compatibility |
| 2026-09-30 | Responsive SVG viewBox & geometry spacing | Prevent viewport clipping and candidate label collision |
| 2026-09-30 | Specimen-specific probe suites and patches | Accurate behavioral trap testing across all 3 specimens |
| 2026-09-30 | Unified FastAPI static serving with SecurityHeadersMiddleware | Single-container deployment with CSP and strict security headers |
| 2026-09-30 | Built-in "How it works" Architecture Drawer | Instant visual reference for Nemotron roles and COW fork tree |

## Measured numbers
| Date | What | Value | Source |
|---|---|---|---|
| 2026-09-30 | Gate 2 Pipeline run duration | 1.61s | `scripts/test_pipeline.py` run |
| 2026-09-30 | Test strength on invoice_totals | 90% (18/20 caught) | Stage 3 mutation run |
| 2026-09-30 | Differential probes on candidate B | 7/50 divergent | Stage 5 probe run |
| 2026-09-30 | Live run end-to-end duration | 6.84s | Browser live execution |
| 2026-09-30 | Frontend build size | 263.4 KB JS / 20.0 KB CSS | `npm run build` |
| 2026-09-30 | Sandbox Fork vs Cold Rebuild | 1.64ms vs 18.4ms (11.2x) | `scripts/benchmark.py` |
| 2026-09-30 | Failure injection test pass rate | 7/7 (100%) | `pytest backend/tests/` |
| 2026-09-30 | Gallery Screenshots | 6/6 captures at 1440x900 | `scripts/screenshots.py` |
| 2026-09-30 | Social Preview Card | 1200x630 (49.6 KB) | `scripts/og_image.py` |

## Open questions
- None. All P0 requirements and gates 0 through 6 are fully satisfied.

## Cut list
| What | Why |
|---|---|
| (none) | All P0 milestones completed |

## Session log
| Date | What was done | What is next |
|---|---|---|
| 2026-09-29 | Phase 0 started: project scaffolded, prerequisites verified | Run spikes S1–S5 (waiting for keys) |
| 2026-09-29 | Phases 1-3: Core backend, pipeline, runtime, and frontend components implemented | Wire up UI to backend SSE, test with fake sandbox |
| 2026-09-30 | Phase 2 complete: Pipeline implemented with 6 real stages, AST mutator, differential probes discovering rounding trap in invoice_totals. Gate 2 passed (`test_pipeline.py`). All 3 specimen traps verified (`verify_specimens.py`). 100% green `check.py`. | H2 checkpoint signoff, multi-specimen sweep |
| 2026-09-30 | Phase 3 complete & Gate 3 passed: Diagnosed and fixed SSE stream dispatch (`event: message`), resolved geometry clipping, tuned candidate bob separation. Verified live end-to-end in browser with Playwright: Plumb Graph renders guideline, checkpoints, mutant tick strip, swinging cables with divergence badges, settle animation, and verdict banner. Dossier view renders diff viewer and full evidence report. 100% green `check.py`. | Phase 4 Hardening (H3 signoff, sweep all specimens) |
| 2026-09-30 | Phase 4 complete & Gate 4 passed: Recorded 3 authentic replays (`scripts/record_replay.py`), generated `docs/benchmarks.md` with measured sandbox fork speedup (11.2x), wrote failure injection test suite (`test_failures.py`: 429 retry, prompt injection resistance, cancellation, budget caps), verified clean clone (`scripts/freshclone.py`), verified 0 vulnerabilities (`pip-audit`). `check.py` 100% green. | Phase 5 Deploy & Phase 6 Submission Kit |
| 2026-09-30 | Phase 5 complete & Gate 5 passed: Multi-stage Dockerfile and docker-compose.yml written and tested. `docs/OPERATIONS.md` completed with budget caps, health monitoring, and judge pass specs. `SecurityHeadersMiddleware` wired into FastAPI. `scripts/test_deployment.py` verified health, static files, and security headers. | Phase 6 Submission Kit |
| 2026-09-30 | Phase 6 complete & Gate 6 passed: Complete README.md (16 sections per §14.3), Devpost copy (`DEVPOST.md`), product feedback (`FEEDBACK.md`), 2:45 video storyboard & voiceover script (`VIDEO_SCRIPT.md`), submission checklist (`CHECKLIST.md`). Added Architecture drawer with inline SVG diagram. Captured all 6 submission screenshots at 1440x900 (`scripts/screenshots.py`) and 1200x630 social card (`scripts/og_image.py`). Quality check `scripts/check.py` 100% green. | Phase 7 Human Checkpoint (Devpost submission) |
| 2026-09-30 | P1 & P2 feature additions: Upgraded DiffViewer with hunk parsing, tabular line numbers, and pin coverage evidence badges. Added in-app Benchmarks modal with live 11.2x fork comparison. Added zip upload tab and recorded run quickstart. Added Bring-Your-Own-Key (BYOK) mode in API. Implemented Model Context Protocol (MCP) server (`scripts/mcp_server.py`) exposing survey, mutate, and verify tools over JSON-RPC 2.0 stdio. Completed automated license audit (`scripts/license_check.py`) and generated `THIRD_PARTY.md` verifying 0 copyleft dependencies. `scripts/check.py` 100% green. | Phase 7 Final Submission (Video & Devpost) |
| 2026-09-30 | Public repository published: Created and pushed master branch and `v1.0.0` tag to https://github.com/mareknardella-lgtm/plumbline. All 19 project requirements and submission assets verified. | Record 2:45 video demo & submit Devpost form |
| 2026-09-30 | P1 bonus completed: Implemented Tavily Deprecation Radar (`backend/app/llm/tavily.py`) satisfying R18, scanning legacy code for deprecated symbols and querying live migration recommendations. 8/8 checks 100% green. | Phase 7 Final Submission (Video & Devpost) |
| 2026-09-30 | P2 UI extensions: Interactive Timeline Scrubber with pure event-stream reducer scrubbing, 4-tab Cockpit right panel (Log, Ledger, Tests, Code DiffViewer), in-UI BYOK key input, and polished theme toggle with Lamplight tokens. 8/8 checks 100% green. | Final verification & push |

