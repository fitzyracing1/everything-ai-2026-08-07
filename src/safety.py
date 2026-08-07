"""
Safety guard inspired by subsumption architecture + decision audit log.

Priority order (higher wins):
1. Provide air / life-support / environment integrity
2. Eat / energy / self-maintenance
3. Win / mission accomplishment
4. Talk / reporting / human legibility

Also records every significant decision for later query.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class SafetyGuard:
    """Very lightweight keyword filter + priority reminder."""

    BLOCKED = {
        "weapon construction", "explosive recipe", "biological agent",
        "child sexual", "self-harm method", "doxxing", "ransomware",
    }

    def allow(self, goal: str) -> bool:
        g = goal.lower()
        for bad in self.BLOCKED:
            if bad in g:
                return False
        return True

    def priority_layer(self, goal: str) -> str:
        g = goal.lower()
        if any(w in g for w in ("air", "oxygen", "life support", "habitat")):
            return "ProvideAir"
        if any(w in g for w in ("energy", "power", "battery", "food", "maintain")):
            return "Eat"
        if any(w in g for w in ("mission", "intercept", "defend", "win", "goal")):
            return "Win"
        return "Talk"


class DecisionAudit:
    """Append-only JSONL audit log."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: str, data: Dict[str, Any] | None = None) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "data": data or {},
        }
        with self.path.open("a") as f:
            f.write(json.dumps(record, default=str) + "\n")
