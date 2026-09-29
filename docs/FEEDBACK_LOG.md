# Feedback log

One entry per friction point or delight with Nebius Token Factory, Sandboxes, AI Cloud, NVIDIA models and tools.

| Date | Product | What happened | Expected vs actual | Severity | Steps to reproduce | Evidence | Suggested fix |
|---|---|---|---|---|---|---|---|
| 2026-09-30 | Token Factory Sandboxes | Token WhoAmI returns `permissions={'spawn': False}` on freshly created static API key | Expected standard hackathon API key to have sandbox spawn rights; actual returns false | Medium | Call `Contree.get_token_info()` with standard static API key | `WhoAmI(permissions={'spawn': False, ...})` | Auto-grant sandbox trial permissions to hackathon participants or provide clear UI prompt |
