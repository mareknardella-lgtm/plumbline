# Plumbline: Final Submission Checklist (§15.5)

Ensure every item below is verified before submitting the Devpost form.

---

## 1. Rules and Eligibility
- [x] Official Rules read and accepted; eligibility confirmed; track selected: **Coding and Agentic Engineering**.
- [x] Project created from scratch within the official hackathon window (26 Aug to 30 Oct 2026), stated in `README.md` and Devpost.
- [x] All submission materials (UI, documentation, code comments, video script) are in English.
- [x] Built without sponsor funding, external contract, or commercial licenses from Nebius or Devpost.

---

## 2. Project & Technical Integration
- [x] Runs on Nebius Token Factory inference with runtime calls verified in ledger.
- [x] Utilizes NVIDIA Nemotron 3 open models (`Nemotron-3-Ultra-550b-a55b`, `nemotron-3-super-120b-a12b`, `NVIDIA-Nemotron-3-Nano-30B-A3B`).
- [x] Token Factory Sandboxes are central to the pipeline (copy-on-write baseline forks, AST mutant verification, test execution).
- [x] Original work; all third-party dependencies cataloged in `docs/THIRD_PARTY.md`; no copied code.
- [x] Single quality command `uv run python scripts/check.py` passes 100% green.

---

## 3. Demo & Operations
- [x] Zero-auth public access: no login or signup needed to run or inspect.
- [x] Dual-mode execution: Live Token Factory runs and high-fidelity Replays ($1\times, 2\times, 4\times$) both supported.
- [x] Budget guards, daily spending caps, and emergency kill switches implemented and tested.
- [x] Healthcheck endpoint `/api/health` returns `200 OK` for automated uptime monitors.
- [x] Static frontend bundled directly with FastAPI backend via `frontend/dist` and `Dockerfile`.

---

## 4. Repository & Open Source
- [x] Open-source MIT License present in root `LICENSE` file.
- [x] Comprehensive `README.md` complete per §14.3 with architecture diagram, Nemotron table, and judge instructions.
- [x] Secret scanning verified via `scripts/freshclone.py`: zero API keys or secrets in repository.
- [x] Dependency vulnerability audit passes clean (`pip-audit`: 0 vulnerabilities).
- [x] All Windows PowerShell commands verified without bash-only scripts.

---

## 5. Video & Media
- [x] Script and storyboard drafted in `docs/submission/VIDEO_SCRIPT.md` (length $< 3:00$).
- [x] Narration covers both Nebius Token Factory and NVIDIA Nemotron roles with measured metrics.
- [x] 6 official screenshots captured at $1440 \times 900$ in light theme saved in `docs/images/`.

---

## 6. Devpost Form
- [x] Complete text prepared in `docs/submission/DEVPOST.md` (700–1000 words).
- [x] Comprehensive feedback section ready in `docs/submission/FEEDBACK.md`.
- [x] Testing instructions for judges clearly laid out with zero setup friction.
