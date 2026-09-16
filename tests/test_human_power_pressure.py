import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
MODULE = ROOT / "experiments/human-power-pressure/run.py"
spec = importlib.util.spec_from_file_location("human_power_pressure", MODULE)
hp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hp)
FIXTURE_FILE = ROOT / "experiments/human-power-pressure/fixtures.json"
FIXTURES = {item["variant"]: item for item in json.loads(FIXTURE_FILE.read_text(encoding="utf-8"))}


class HumanPowerPressureTests(unittest.TestCase):
    def load(self, variant):
        return json.loads(json.dumps(FIXTURES[variant]))

    def test_bundled_fixtures_are_structurally_valid_and_complete(self):
        package = hp.run([FIXTURE_FILE], producer_revision="a" * 40)
        self.assertGreaterEqual(package["case_count"], 10)
        self.assertEqual(0, package["evidence_required_count"])
        self.assertEqual(
            {"disclosure", "correlation", "refusal", "decision-feature"},
            {r["case"]["family"] for r in package["results"]},
        )

    def test_missing_runtime_observation_is_evidence_required_not_pass(self):
        fixture = self.load("stable-demand")
        fixture["observations"]["correlation"].pop("observer_evidence")
        result = hp.build_result(fixture, producer_revision="b" * 40)
        self.assertEqual("EVIDENCE_REQUIRED", result["evidence_state"])
        self.assertIn("observations.correlation.observer_evidence", result["missing_observations"])
        self.assertNotIn("PASS", result["evidence_state"])

    def test_output_contains_no_normative_score_or_judgment(self):
        result = hp.build_result(self.load("service-denial"), producer_revision="c" * 40)
        encoded = json.dumps(result).lower()
        for forbidden in (
            "harm_score",
            "privacy_score",
            "discrimination_score",
            '"legitimate":',
            '"coercive":',
        ):
            self.assertNotIn(forbidden, encoded)
        self.assertIn("a harm or discrimination judgment", result["claim_boundary"]["does_not_support"])

    def test_disclosure_comparison_keeps_same_task(self):
        fixtures = [
            self.load("minimal"),
            self.load("expanded"),
            self.load("governed-enhanced-assurance"),
        ]
        hp.validate_comparison_groups(fixtures)
        expanded = hp.build_result(fixtures[1], producer_revision="d" * 40)
        self.assertEqual(
            ["date_of_birth", "full_name", "home_address"],
            expanded["derived_signals"]["requested_beyond_available_minimal"],
        )

    def test_comparison_group_rejects_task_semantic_drift(self):
        fixtures = [self.load("minimal"), self.load("expanded")]
        fixtures[1]["task"]["semantics"] = "different consequential task"
        with self.assertRaisesRegex(ValueError, "changes task identity or semantics"):
            hp.validate_comparison_groups(fixtures)

    def test_correlation_escalation_is_observed_not_judged(self):
        result = hp.build_result(self.load("cross-session-observed"), producer_revision="e" * 40)
        self.assertTrue(result["derived_signals"]["scope_changed_from_declared"])
        self.assertEqual("pairwise", result["derived_signals"]["declared_scope"])
        self.assertEqual("cross-session-stable", result["derived_signals"]["effective_scope"])

    def test_refusal_pressure_signals_preserve_authorization_boundary(self):
        result = hp.build_result(self.load("prompt-loop"), producer_revision="f" * 40)
        self.assertEqual(3, result["derived_signals"]["prompt_count_after_refusal"])
        self.assertTrue(result["observations"]["authorization"]["validity_observed"])
        self.assertIn("a legitimacy or consent judgment", result["claim_boundary"]["does_not_support"])

    def test_undeclared_decision_feature_is_machine_visible(self):
        result = hp.build_result(self.load("hidden-community"), producer_revision="1" * 40)
        self.assertEqual(
            ["community_membership"],
            result["derived_signals"]["undeclared_evaluated_features"],
        )

    def test_malformed_family_is_rejected(self):
        fixture = self.load("minimal")
        fixture["family"] = "opinion"
        with self.assertRaisesRegex(ValueError, "family must be one of"):
            hp.validate_fixture(fixture)


if __name__ == "__main__":
    unittest.main()
