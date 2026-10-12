# Everything AI (2026-08-07 snapshot)

The README describes a modular agent framework that turns natural-language goals into artifacts.

## What is in the repo

| File | Role |
|---|---|
| `src/main.py` | CLI: `--goal/-g`, `--root`, `--max-steps` (default 8). With no goal it starts interactive mode |
| `src/agent.py` | `EverythingAgent.run(goal, max_steps)`, `interactive()` |
| `src/planner.py` | `Planner.plan(goal)` |
| `src/safety.py` | `SafetyGuard.allow()`, `priority_layer()`, `DecisionAudit` |
| `tests/test_smoke.py` | unittest smoke tests |

**Known gap:** `src/agent.py` imports `.coder`, but `src/coder.py` is not committed. As a result `python -m src.main --goal "..."` fails with `ModuleNotFoundError: No module named 'src.coder'` (checked on a clean clone), and so do the smoke tests that import the agent. The README's quick start also uses the original sandbox path.

The repo has no CI and no LICENSE file. Copyright (c) 2026 Joshua Almeida
