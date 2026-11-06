import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "bidcheck.py"
FIXTURES = ROOT / "examples" / "northstar" / "fixtures"


def run_fixture(name: str, md_path: Path | None = None) -> subprocess.CompletedProcess:
    command = [sys.executable, str(CLI), str(FIXTURES / name)]
    if md_path is not None:
        command.extend(["--md", str(md_path)])
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def run_data(data: dict, md_path: Path | None = None) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "decision.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        command = [sys.executable, str(CLI), str(path)]
        if md_path is not None:
            command.extend(["--md", str(md_path)])
        return subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )


def valid_partner_data() -> dict:
    return json.loads((FIXTURES / "valid_partner.json").read_text(encoding="utf-8"))


class BidcheckTests(unittest.TestCase):
    def test_valid_partner(self):
        result = run_fixture("valid_partner.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)
        self.assertIn("bid_with_partner", result.stdout)
        self.assertIn("68/100", result.stdout)

    def test_valid_partner_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "decision-record.md"
            result = run_fixture("valid_partner.json", md_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(md_path.exists())
            text = md_path.read_text(encoding="utf-8")
            self.assertIn("# Bid Decision Record", text)
            self.assertIn("Bid with partner", text)
            self.assertIn("Priya Raman", text)
            self.assertIn("## Conditions", text)
            self.assertIn("VP Finance margin exception", text)
            self.assertIn("68", text)
            self.assertIn("## Base gates", text)
            self.assertIn("## Partner gates", text)
            self.assertIn("**Margin exception:**", text)
            self.assertIn("Approved by:", text)
            self.assertIn("**Human approval reference:**", text)
            self.assertIn("**Fallback:**", text)

    def test_valid_no_bid(self):
        result = run_fixture("valid_no_bid.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no_bid", result.stdout)
        self.assertIn("46/100", result.stdout)

    def test_invalid_missing_evidence(self):
        result = run_fixture("invalid_missing_evidence.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires evidence", result.stderr)

    def test_invalid_low_bid(self):
        result = run_fixture("invalid_low_bid.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires total_score at least 65", result.stderr)

    def test_invalid_not_assessed_g1(self):
        data = valid_partner_data()
        for requirement in data["requirements"] + data["base_requirements"]:
            if requirement["id"] == "M1":
                requirement["status"] = "not_assessed"
        for gate in data["gates"] + data["base_gates"]:
            if gate["id"] == "G1":
                gate["status"] = "pass_with_conditions"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing, conflicting, or not assessed", result.stderr)

    def test_invalid_agent_human_owner(self):
        data = valid_partner_data()
        data["human_owner"] = "bid-analyst"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("human_owner must name a human decision owner", result.stderr)

    def test_invalid_placeholder_approval(self):
        data = valid_partner_data()
        data["human_approval_ref"] = "n/a"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholders are not accepted", result.stderr)

    def test_invalid_placeholder_margin_reference(self):
        data = valid_partner_data()
        data["margin_exception"]["record_ref"] = "n/a"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("margin_exception.record_ref must identify a real record", result.stderr)

    def test_invalid_placeholder_conditions(self):
        data = valid_partner_data()
        for index, condition in enumerate(data["conditions"], start=1):
            condition["text"] = f"Placeholder condition {index}"
            condition["owner"] = "n/a"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("conditions must cover", result.stderr)
        self.assertIn("must be substantive", result.stderr)

    def test_invalid_model_human_owner(self):
        for name in (
            "Claude Code",
            "GPT-4",
            "OpenAI",
            "AutoGPT",
            "Bid Analyst",
            "Bid Critic",
        ):
            with self.subTest(name=name):
                data = valid_partner_data()
                data["human_owner"] = name
                result = run_data(data)
                self.assertEqual(result.returncode, 1)
                self.assertIn(
                    "human_owner must name a human decision owner", result.stderr
                )

    def test_invalid_model_margin_approver(self):
        data = valid_partner_data()
        data["margin_exception"]["approved_by"] = "GPT-4"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("margin_exception.approved_by must name a human approver", result.stderr)

    def test_invalid_model_condition_owner(self):
        for name in ("Claude Code", "Bid Analyst", "Bid Critic"):
            with self.subTest(name=name):
                data = valid_partner_data()
                for condition in data["conditions"]:
                    condition["owner"] = name
                result = run_data(data)
                self.assertEqual(result.returncode, 1)
                self.assertIn(
                    "owner must name a human or accountable role", result.stderr
                )

    def test_invalid_project_agent_margin_approver(self):
        data = valid_partner_data()
        data["margin_exception"]["approved_by"] = "Bid Analyst"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "margin_exception.approved_by must name a human approver", result.stderr
        )

    def test_invalid_project_agent_gate_approver(self):
        data = valid_partner_data()
        for gate in data["gates"]:
            if gate["id"] == "G1":
                gate["status"] = "fail"
        data["gate_exceptions"] = [
            {
                "gate_id": "G1",
                "approved_by": "Bid Analyst",
                "approved_by_role": "Pursuit Lead + Accountable Executive",
                "reason": "Test exception with an agent approver.",
                "date": "2026-10-24",
                "record_ref": "Room message from the test fixture, 2026-10-24.",
            }
        ]
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("approved_by must name a human approver", result.stderr)

    def test_invalid_agent_approval_reference(self):
        data = valid_partner_data()
        data["human_approval_ref"] = (
            "Claude Code approved this record in a session message on 2026-10-24"
        )
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not claim an agent approved", result.stderr)

    def test_invalid_agent_rationale(self):
        data = valid_partner_data()
        data["rationale"] = "The bid is approved and submitted by the agent."
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not claim an agent approved", result.stderr)

    def test_invalid_project_agent_approval_reference(self):
        data = valid_partner_data()
        data["human_approval_ref"] = "Bid Analyst approved the bid on 2026-10-24"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not claim an agent approved", result.stderr)

    def test_invalid_project_agent_rationale(self):
        data = valid_partner_data()
        data["rationale"] = "Bid Critic approved the bid and submitted it."
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not claim an agent approved", result.stderr)

    def test_invalid_real_client_data_note(self):
        data = valid_partner_data()
        data["data_note"] = "This is synthetic, but includes real client data."
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("must affirm synthetic data", result.stderr)

    def test_valid_negated_agent_claim(self):
        data = valid_partner_data()
        data["rationale"] = (
            "The human owner approved the conditional route. "
            "No agent approved, priced, submitted, or contacted the buyer."
        )
        result = run_data(data)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_invalid_base_partner_covered(self):
        data = valid_partner_data()
        for requirement in data["base_requirements"]:
            if requirement["id"] in {"M1", "M2", "M4"}:
                requirement["status"] = "partner_covered"
        for gate in data["base_gates"]:
            if gate["id"] == "G1":
                gate["status"] = "pass"
        result = run_data(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("base_requirements must describe Meridian alone", result.stderr)

    def test_invalid_gate_requirement_mismatch(self):
        result = run_fixture("invalid_gate_requirement.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("G1 cannot be pass", result.stderr)

    def test_invalid_one_gate(self):
        result = run_fixture("invalid_one_gate.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must contain exactly G1-G6", result.stderr)

    def test_invalid_fake_gate(self):
        result = run_fixture("invalid_fake_gate.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must contain exactly G1-G6", result.stderr)

    def test_invalid_one_requirement(self):
        result = run_fixture("invalid_one_requirement.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must contain exactly M1-M6", result.stderr)

    def test_invalid_negative_data_note(self):
        result = run_fixture("invalid_negative_data_note.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must affirm synthetic data", result.stderr)

    def test_invalid_base_score_consistency(self):
        result = run_fixture("invalid_base_score.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Base G2 must be fail", result.stderr)

    def test_invalid_gate_exception_completeness(self):
        result = run_fixture("invalid_gate_exception.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires date", result.stderr)

    def test_invalid_base_g1(self):
        result = run_fixture("invalid_base_g1.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Base G1 cannot be pass", result.stderr)

    def test_invalid_base_g3(self):
        result = run_fixture("invalid_base_g3.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Base G3 cannot be pass", result.stderr)

    def test_invalid_margin_approver(self):
        result = run_fixture("invalid_margin_approver.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("approved_by_role must be 'VP of Finance'", result.stderr)

    def test_invalid_extra_score(self):
        result = run_fixture("invalid_extra_score.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unknown score criteria", result.stderr)

    def test_invalid_g1_pass_with_conditions(self):
        result = run_fixture("invalid_g1_conditions.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("G1 cannot be pass", result.stderr)

    def test_invalid_policy_margin_constant(self):
        result = run_fixture("invalid_policy_margin.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("policy_min_margin_percent must be 15", result.stderr)

    def test_invalid_nonpolicy_weights(self):
        result = run_fixture("invalid_nonpolicy_weights.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("weight must be", result.stderr)

    def test_invalid_one_condition(self):
        result = run_fixture("invalid_one_condition.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("full nine-condition set", result.stderr)

    def test_invalid_final_g4(self):
        result = run_fixture("invalid_final_g4.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("G4 cannot be pass while M4", result.stderr)

    def test_invalid_gate_exception_authority(self):
        result = run_fixture("invalid_gate_exception_authority.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("approved_by_role must be", result.stderr)

    def test_invalid_gate_override(self):
        result = run_fixture("invalid_gate_override.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires a recorded human gate exception", result.stderr)

    def test_invalid_weights(self):
        result = run_fixture("invalid_weights.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must sum to 100", result.stderr)

    def test_invalid_human_signoff(self):
        result = run_fixture("invalid_human_signoff.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("human_signoff must be true", result.stderr)

    def test_invalid_margin(self):
        result = run_fixture("invalid_margin.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("margin_exception is required", result.stderr)

    def test_invalid_conditions(self):
        result = run_fixture("invalid_conditions.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires the full nine-condition set", result.stderr)

    def test_invalid_score(self):
        result = run_fixture("invalid_score.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not match computed", result.stderr)

    def test_invalid_data_note(self):
        result = run_fixture("invalid_data_note.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("fictional or synthetic", result.stderr)

    def test_invalid_decision(self):
        result = run_fixture("invalid_decision.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid decision", result.stderr)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text("{", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CLI), str(bad)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid JSON", result.stderr)

    def test_missing_file(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "no-such-file.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("could not read", result.stderr)


if __name__ == "__main__":
    unittest.main()
