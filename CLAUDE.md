# Plumbline: Nebius x NVIDIA Global AI Hackathon, Coding and Agentic Engineering track
Read docs/MASTER_PROMPT.md first; it is the source of truth. Then docs/PROGRESS.md for current state.
Always:
- Deadline: 30 Oct 2026, 10:00 PT. Aim to submit by 27 Oct.
- Never guess an API: read the docs, spike, run. The docs win over the prompt; log differences in docs/SPIKE_NOTES.md.
- Never invent numbers, quotes or results. Every claim comes from a run log or docs/benchmarks.md.
- Never commit secrets. Keys live only in .env.
- User code runs only inside Token Factory Sandboxes, never on the host or in the backend process.
- Windows PowerShell must work: no Make, no bash-only scripts.
- One quality command: uv run python scripts/check.py
- Update docs/PROGRESS.md at the end of each session. Log friction in docs/FEEDBACK_LOG.md.
- Finish P0 before P1. Stop at the gates and human checkpoints (sections 16 and 17).
