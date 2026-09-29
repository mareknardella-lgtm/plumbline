# Plumbline

**Refactor old code without changing what it does, and see the evidence.**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 🚧 Under active development for the Nebius × NVIDIA Global AI Hackathon (Coding and Agentic Engineering track).

## 1. Title

Plumbline records how your code behaves today, plants bugs in it to check that record, then tests every refactor against it and shows the evidence.

## 2. Try it

*(Live demo URL and setup instructions will be added in Phase 5.)*

### Run locally (replay-only, no keys needed)

```powershell
git clone https://github.com/YOUR_USERNAME/plumbline.git
cd plumbline
uv sync
cd frontend && npm install && npm run build && cd ..
uv run uvicorn backend.app.main:app --port 8000
# Open http://localhost:8000
```

### Run locally (live mode, requires keys)

```powershell
cp .env.example .env
# Fill in NEBIUS_API_KEY and NEBIUS_AI_PROJECT
uv run uvicorn backend.app.main:app --port 8000
```

## 3. What it does

Teams avoid refactoring legacy code because nothing tells them whether behavior survived. AI refactors make this worse: they read well, pass the tests the same model wrote, and still change behavior in corners nobody checked.

**Plumbline** gives you a piece of Python code and a goal, then:
1. Records how the code behaves today
2. Plants bugs to test the tests
3. Tries several refactors in isolated sandboxes
4. Compares each one with the original on unseen inputs
5. Returns a patch plus a dossier that says what was checked and what was not

### What makes it different
1. **Evidence, not vibes.** Every verdict is backed by artifacts a reviewer can re-run.
2. **Tests are tested.** A deterministic AST mutator plants bugs; the behavior tests must catch them.
3. **Sandboxes as an experimental instrument.** Fork and measure, not fork and pick the best.
4. **Model tiering by role.** Nemotron 3 Ultra plans and judges, Super writes code, Nano does high-volume work.
5. **Honest limits.** The dossier ends with what the evidence does not cover.

## 4. How it works

*(Pipeline diagram and architecture details will be added in Phase 1.)*

## 5. NVIDIA Nemotron

*(Model table with measured values will be added in Phase 2.)*

## 6. Nebius Token Factory

*(Token Factory usage details will be added in Phase 2.)*

## 7. Other Nebius tools and services

*(Details will be added as services are integrated.)*

## 8. Results and limits

*(Benchmark results will be added in Phase 4.)*

## 9. Quick start

See section 2 above.

## 10. Configuration

See [.env.example](.env.example) for all configuration variables.

## 11. Development

```powershell
# Quality check
uv run python scripts/check.py

# Run backend in dev mode
uv run uvicorn backend.app.main:app --reload --port 8000

# Run frontend in dev mode
cd frontend && npm run dev
```

## 12. Built during the submission period

This project was created after 26 Aug 2026. First commit date and hash will be recorded here after initialization.

## 13. Deployment

*(Deployment instructions will be added in Phase 5.)*

## 14. Security and data handling

See [SECURITY.md](SECURITY.md).

## 15. Feedback and thanks

See [docs/submission/FEEDBACK.md](docs/submission/FEEDBACK.md) for our feedback on the tools.

Thank you to Nebius, NVIDIA and Tavily.

## 16. License

[MIT](LICENSE). Third-party notices in [THIRD_PARTY.md](THIRD_PARTY.md).
