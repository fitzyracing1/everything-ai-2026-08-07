"""
Simple rule-based planner that decomposes a natural-language goal
into a short sequence of concrete steps.

Presumed need: Fastest path from goal string to ordered executable steps
without requiring an external LLM call for the first production version.
"""

from __future__ import annotations

from typing import Any, Dict, List


class Planner:
    """Heuristic goal decomposer."""

    KEYWORDS = {
        "api": ["create_rest_api", "add_endpoints", "write_tests"],
        "cli": ["create_cli", "add_commands", "persist_data"],
        "web": ["create_html", "add_css", "serve_static"],
        "simulation": ["create_simulation", "add_physics", "run_demo"],
        "monorepo": ["scaffold_monorepo", "add_packages", "write_scan_md"],
        "agent": ["create_agent_class", "add_loop", "add_safety"],
        "skill": ["scaffold_skill", "write_skill_md", "add_scripts"],
        "test": ["write_tests", "run_tests"],
        "doc": ["write_readme", "write_docs"],
        "github": ["create_repo", "push_files"],
        "build": ["scaffold_project", "write_core", "add_entry"],
        "everything": ["scaffold_everything", "integrate_skills", "add_persistence"],
        "todo": ["create_cli", "add_commands", "persist_data"],
    }

    def plan(self, goal: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        goal_l = goal.lower()
        steps: List[Dict[str, Any]] = []

        # Always start with a light scan if nothing exists yet
        if not context or not context.get("files"):
            steps.append({
                "name": "initial_scan",
                "type": "scan",
                "description": "Scan sandbox and skills",
            })

        matched = False
        for key, actions in self.KEYWORDS.items():
            if key in goal_l:
                matched = True
                for action in actions:
                    steps.append({
                        "name": action,
                        "type": "code" if "create" in action or "write" in action or "scaffold" in action else "compose",
                        "description": f"Auto-generated step for keyword '{key}'",
                        "goal_fragment": goal,
                    })

        if not matched:
            # Generic fallback – always produce something useful
            steps.extend([
                {
                    "name": "scaffold_project",
                    "type": "code",
                    "description": "Create minimal project skeleton for the goal",
                    "goal_fragment": goal,
                },
                {
                    "name": "write_core_module",
                    "type": "code",
                    "description": "Write a core Python module implementing the intent",
                    "goal_fragment": goal,
                },
                {
                    "name": "write_readme",
                    "type": "code",
                    "description": "Document the deliverable",
                    "goal_fragment": goal,
                },
            ])

        # Always finish with a summary artifact
        steps.append({
            "name": "finalize_summary",
            "type": "code",
            "description": "Write a machine-readable summary of what was built",
            "goal_fragment": goal,
        })

        return {
            "goal": goal,
            "steps": steps,
            "strategy": "keyword_heuristic_v1",
        }
