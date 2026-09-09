import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "experiments/vti-trust-task-credential-path/evaluate.py"
spec = importlib.util.spec_from_file_location("vti_tt_credential", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VtiTrustTaskCredentialPathTests(unittest.TestCase):
    def test_source_evidence_narrows_composition_without_claiming_runtime_effect(self):
        observations = {
            "trust_task_type": True,
            "credential_write_gate": True,
            "independent_signing_context": True,
            "vac_constructor": True,
            "empty_actions_fail_closed": True,
            "credential_response": True,
            "target_package_tests": "passed",
            "behavior_test_present": False,
        }
        result = module.evaluate(observations, "1d9d3672c4a538c84b8263229619ae3bb4342b26")
        self.assertEqual("SOURCE_PINNED_INTEGRATION_EVIDENCE", result["evidence_maturity"])
        self.assertEqual("PARTIALLY_DISCHARGED", result["r001"])
        self.assertEqual("PARTIALLY_DISCHARGED", result["r002"])
        self.assertIn("behavioral target-native test", result["remaining_gap"])
        self.assertIn("future consequential authority", result["claim_boundary"])

    def test_missing_boundary_observation_fails_closed(self):
        observations = {
            "trust_task_type": True,
            "credential_write_gate": False,
            "independent_signing_context": True,
            "vac_constructor": True,
            "empty_actions_fail_closed": True,
            "credential_response": True,
            "target_package_tests": "passed",
            "behavior_test_present": False,
        }
        with self.assertRaises(ValueError):
            module.evaluate(observations, "1d9d3672c4a538c84b8263229619ae3bb4342b26")


if __name__ == "__main__":
    unittest.main()
