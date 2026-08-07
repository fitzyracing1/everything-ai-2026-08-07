# Everything AI

**Build everything with AI.**

A production-ready, modular, self-extending AI agent framework designed to operate entirely inside the Grok sandbox (or any Python environment).  
It turns natural-language goals into working code, tools, documents, simulations, and complete systems by composing existing skills, generating new modules, and maintaining a persistent delivery loop.

## Core Capabilities

- **Goal → Artifact**: Accept any high-level goal ("build a REST API for X", "simulate ballistic trajectories", "create a monorepo of knowledge", "design a subsumption controller") and produce runnable code + docs.
- **Skill Integration**: Automatically discovers and can invoke or extend the local skill library under `~/.grok/skills`.
- **Persistent Self-Coding**: Continuously scans for gaps (TODOs, stubs, missing tests) and delivers improvements without further prompting.
- **Tool Composition**: Uses Starfit-style live header grabbing and topological execution for dynamic workflows.
- **Offline-first**: All heavy lifting happens locally; external tools only for initial knowledge acquisition when needed.
- **Safety Layers**: Subsumption-style priority (air → energy → mission → talk) and decision audit logging.

## Quick Start

```bash
cd /home/workdir/artifacts/everything-ai
python -m src.main --goal "build a simple todo CLI with persistent storage"
```

Or interactive mode:

```bash
python -m src.main
```

## Project Layout

```
everything-ai/
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point + CLI
│   ├── agent.py             # Core EverythingAgent
│   ├── planner.py           # Goal decomposition & planning
│   ├── coder.py             # Code generation & file writing
│   ├── scanner.py           # Environment & skill scanner
│   ├── composer.py          # Starfit-inspired tool composer
│   └── safety.py            # Subsumption + audit
├── skills_integration/      # Adapters for local skills
├── tests/
├── docs/
└── artifacts/               # Runtime generated outputs (created on first run)
```

## Design Philosophy

1. **Fastest path to production** – every response must leave a usable artifact.
2. **Presume needs from evidence** – never wait for perfect specs.
3. **Self-maintaining** – the agent improves its own codebase over time.
4. **Composable** – new capabilities are just new tools registered with triggers and grabs.
5. **Human-legible** – every generated file carries the reasoning that produced it.

## Next Increments (already queued for the persistent loop)

- Full Starfit runtime embedding
- Automatic GitHub repo creation + push for every significant deliverable
- Multi-agent swarm mode (BMD-style coordination)
- Voice interface via connected tools
- Visual branding pipeline integration

---

Built autonomously by the Grok persistent self-coder + sandbox open-ended solver on 2026-08-07.
