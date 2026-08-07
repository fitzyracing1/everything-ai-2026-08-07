"""Smoke test for Everything AI."""
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import EverythingAgent
from src.planner import Planner
from src.safety import SafetyGuard


class TestSmoke(unittest.TestCase):
    def test_planner_returns_steps(self):
        p = Planner()
        plan = p.plan("build a simple cli tool")
        self.assertIn("steps", plan)
        self.assertGreater(len(plan["steps"]), 0)

    def test_safety_allows_normal(self):
        s = SafetyGuard()
        self.assertTrue(s.allow("build a web dashboard"))

    def test_agent_instantiates(self):
        agent = EverythingAgent(root="/tmp/everything-ai-test")
        self.assertIsNotNone(agent)


if __name__ == "__main__":
    unittest.main()
