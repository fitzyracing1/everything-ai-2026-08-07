#!/usr/bin/env python3
"""
Everything AI – CLI entry point.

Usage:
  python -m src.main --goal "build a todo CLI"
  python -m src.main                 # interactive
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure package is importable when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import EverythingAgent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Everything AI – Build everything with AI")
    parser.add_argument("--goal", "-g", type=str, help="Single goal to execute")
    parser.add_argument("--root", type=str, default=None, help="Override project root")
    parser.add_argument("--max-steps", type=int, default=8)
    args = parser.parse_args(argv)

    agent = EverythingAgent(root=args.root)

    if args.goal:
        result = agent.run(args.goal, max_steps=args.max_steps)
        print("\n=== RESULT ===")
        print(f"Status: {result.get('status')}")
        print(f"Artifacts produced: {len(result.get('results', []))}")
        for r in result.get("results", []):
            if "artifact" in r and isinstance(r["artifact"], dict):
                p = r["artifact"].get("path")
                if p:
                    print(f"  • {p}")
        return 0
    else:
        agent.interactive()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
