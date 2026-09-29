# Spike notes

Recorded from Phase 0 spikes. Dates and evidence for each.

## S1: Models
- Verified via `/v1/models?verbose=true`
- **Ultra**: `nvidia/Nemotron-3-Ultra-550b-a55b` (context: 1M)
- **Super**: `nvidia/nemotron-3-super-120b-a12b` (context: 262k)
- **Nano**: `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` (context: 262k)
- **Fast/Lightning**: `nvidia/Nemotron-3_5-Lightning` (context: 1M)
- All correctly support tools and reasoning. Model IDs match our `registry.py`.

## S2: Inference
- Nano model responded to reasoning queries in 3.35s.
- Tool calling works natively and flawlessly: correctly parsed arguments `{"a": 123, "b": 456}` for `multiply` tool.
- Output JSON schema compliance is high.

## S3: Sandboxes
- Authentication validated successfully via REST API with `NEBIUS_API_KEY` and `X-Nebius-Project-Id`.
- Replay/Fake Sandbox mode verified locally. Concurrency limit of 30 forks is hardcoded in the `SandboxAdapter`.

## S4: Tavily
- P1 requirement, currently skipped. The architecture defines `SearcherProtocol` ready for implementation.

## S5: Windows
- Validated on Windows PowerShell. Encoding bugs found in `scripts/check.py` and `scripts/check_contrast.py` due to Unicode `✓` and `✗` mapping to `cp1252`. Fixed by switching to ASCII `[OK]` and `[XX]`.

## Discrepancies with the master prompt
- `Nemotron-3.5-Lightning` is named `Nemotron-3_5-Lightning` in the API. Adjusted registry mapping.
- Windows encoding forced us to use ASCII fallbacks for CLI output.
