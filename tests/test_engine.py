import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bidroom.engine import render_markdown, validate  # noqa: E402
from bidroom.policy import load_policy  # noqa: E402

NORTHSTAR_POLICY = ROOT / "examples" / "northstar" / "policy.json"
NORTHSTAR_DECISION = ROOT / "examples" / "northstar" / "verification" / "decision.example.json"
SIMPLE_POLICY = Path(__file__).resolve().parent / "fixtures" / "policy_simple.json"


def simple_decision() -> dict:
    return {
        "pursuit": "Test pursuit",
        "rfp": "TEST-001",
        "decision": "bid",
        "human_owner": "Alex Doe, Bid Director",
        "human_signoff": True,
        "decision_date": "2026-01-01",
        "data_note": "All data is fictional synthetic sample data.",
        "human_approval_ref": "Room message from Alex Doe, 2026-01-01.",
        "requirements": [
            {
                "id": "R1",
                "text": "Mandatory evidence",
                "status": "met",
                "evidence": "Evidence is in the test packet.",
            }
        ],
        "base_requirements": [
            {
                "id": "R1",
                "text": "Mandatory evidence",
                "status": "met",
                "evidence": "Evidence is in the test packet.",
            }
        ],
        "scores": {
            "fit": {"weight": 60, "score": 4, "evidence": "Strong fit."},
            "price": {"weight": 40, "score": 3, "evidence": "Acceptable price."},
        },
        "base_scores": {
            "fit": {"weight": 60, "score": 4, "evidence": "Strong fit."},
            "price": {"weight": 40, "score": 3, "evidence": "Acceptable price."},
        },
        "total_score": 72.0,
        "base_total_score": 72.0,
        "margin_percent": 25.0,
        "base_margin_percent": 25.0,
        "policy_min_margin_percent": 20.0,
        "gates": [
            {"id": "MANDATORY", "text": "Mandatory evidence", "status": "pass", "evidence": "Met."},
            {"id": "SCORE", "text": "Minimum fit score", "status": "pass", "evidence": "72/100."},
            {"id": "MARGIN", "text": "Minimum margin", "status": "pass", "evidence": "25%."},
            {"id": "APPROVAL", "text": "Human approval", "status": "pass", "evidence": "Recorded."},
        ],
        "base_gates": [
            {"id": "MANDATORY", "text": "Mandatory evidence", "status": "pass", "evidence": "Met."},
            {"id": "SCORE", "text": "Minimum fit score", "status": "pass", "evidence": "72/100."},
            {"id": "MARGIN", "text": "Minimum margin", "status": "pass", "evidence": "25%."},
            {"id": "APPROVAL", "text": "Human approval", "status": "pass", "evidence": "Recorded."},
        ],
        "conditions": [],
        "actions": [
            {
                "text": "Proceed with the bid.",
                "owner": "Alex Doe",
                "due_date": "2026-01-02",
                "status": "open",
            }
        ],
        "rationale": "The test pursuit meets the policy.",
        "uncertainty": "None in the test fixture.",
    }


class EngineTests(unittest.TestCase):
    def test_northstar_policy_loads(self):
        policy = load_policy(NORTHSTAR_POLICY)
        self.assertEqual(policy.policy_id, "northstar-bid-policy")
        self.assertEqual(len(policy.gates), 6)
        self.assertEqual(len(policy.criteria), 4)

    def test_northstar_example_valid(self):
        policy = load_policy(NORTHSTAR_POLICY)
        data = json.loads(NORTHSTAR_DECISION.read_text(encoding="utf-8"))
        self.assertEqual(validate(data, policy), [])

    def test_second_policy_valid(self):
        policy = load_policy(SIMPLE_POLICY)
        self.assertEqual(validate(simple_decision(), policy), [])

    def test_render_uses_policy_labels(self):
        policy = load_policy(SIMPLE_POLICY)
        rendered = render_markdown(simple_decision(), policy)
        self.assertIn("Fit", rendered)
        self.assertIn("MANDATORY", rendered)

    def test_agent_owner_rejected(self):
        policy = load_policy(NORTHSTAR_POLICY)
        data = json.loads(NORTHSTAR_DECISION.read_text(encoding="utf-8"))
        data["human_owner"] = "Bid Analyst"
        errors = validate(data, policy)
        self.assertTrue(any("human decision owner" in error for error in errors))

    def test_base_partner_covered_rejected(self):
        policy = load_policy(SIMPLE_POLICY)
        data = simple_decision()
        data["base_requirements"][0]["status"] = "partner_covered"
        errors = validate(data, policy)
        self.assertTrue(any("base_requirements" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
