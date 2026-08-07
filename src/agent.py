"""
Core EverythingAgent.

Presumed need: A single entry class that can accept any goal, scan the environment,
plan a minimal path, generate code, write files, and log decisions.
Evidence: Empty artifacts/ + user request "Build everything in ai".
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .planner import Planner
from .coder import Coder
from .scanner import Scanner
from .safety import SafetyGuard, DecisionAudit
from .composer import Composer


class EverythingAgent:
    """Autonomous agent that turns goals into working artifacts."""

    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root or "/home/workdir/artifacts/everything-ai")
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "artifacts").mkdir(exist_ok=True)
        (self.root / "logs").mkdir(exist_ok=True)

        self.scanner = Scanner(self.root)
        self.planner = Planner()
        self.coder = Coder(self.root)
        self.composer = Composer(self.root)
        self.safety = SafetyGuard()
        self.audit = DecisionAudit(self.root / "logs" / "decisions.jsonl")

        self.state: Dict[str, Any] = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "goals_completed": [],
            "artifacts_created": [],
        }

    def run(self, goal: str, max_steps: int = 8) -> Dict[str, Any]:
        """Execute a full goal → artifact cycle."""
        print(f"\n[EverythingAI] Goal received: {goal}")
        self.audit.log("goal_received", {"goal": goal})

        # 1. Safety / priority check
        if not self.safety.allow(goal):
            msg = "Goal blocked by safety layer"
            self.audit.log("blocked", {"goal": goal, "reason": msg})
            return {"status": "blocked", "reason": msg}

        # 2. Scan current environment
        scan = self.scanner.scan()
        self.audit.log("scan_complete", {"files": len(scan.get("files", [])), "skills": len(scan.get("skills", []))})

        # 3. Plan
        plan = self.planner.plan(goal, context=scan)
        self.audit.log("plan_created", {"steps": [s["name"] for s in plan["steps"]]})

        # 4. Execute steps
        results = []
        for i, step in enumerate(plan["steps"][:max_steps]):
            print(f"  → Step {i+1}/{len(plan['steps'])}: {step['name']}")
            try:
                if step["type"] == "code":
                    artifact = self.coder.write(step)
                elif step["type"] == "compose":
                    artifact = self.composer.compose(step)
                elif step["type"] == "scan":
                    artifact = self.scanner.scan()
                else:
                    artifact = {"note": f"Unhandled step type {step['type']}"}
                results.append({"step": step["name"], "artifact": artifact})
                self.state["artifacts_created"].append(artifact)
            except Exception as e:
                results.append({"step": step["name"], "error": str(e)})
                self.audit.log("step_error", {"step": step["name"], "error": str(e)})

        # 5. Record completion
        self.state["goals_completed"].append({
            "goal": goal,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "results": results,
        })
        self.audit.log("goal_completed", {"goal": goal, "num_results": len(results)})

        summary = {
            "status": "completed",
            "goal": goal,
            "plan": plan,
            "results": results,
            "state": self.state,
        }
        self._write_summary(summary)
        return summary

    def _write_summary(self, summary: Dict[str, Any]) -> None:
        path = self.root / "artifacts" / f"summary_{int(time.time())}.json"
        path.write_text(json.dumps(summary, indent=2, default=str))
        print(f"[EverythingAI] Summary written → {path}")

    def interactive(self) -> None:
        """Simple REPL for iterative building."""
        print("Everything AI interactive mode. Type a goal or 'quit'.")
        while True:
            try:
                goal = input("\ngoal> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not goal or goal.lower() in {"quit", "exit", "q"}:
                break
            self.run(goal)
        print("Session ended.")
