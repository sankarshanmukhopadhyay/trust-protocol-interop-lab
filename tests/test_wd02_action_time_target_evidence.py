import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "experiments/dtg-vdc-vac-composition/run_action_time.py"
spec = importlib.util.spec_from_file_location("run_action_time", MODULE)
run_action_time = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_action_time)


class Wd02ActionTimeTargetEvidenceTests(unittest.TestCase):
    def test_aligned_component_runtime_narrows_but_does_not_close_composition_gap(self):
        target = {
            "repository": "OpenVTC/dtg-credentials",
            "revision": "985b81042fd7675b14c70af76cb2d009e94618a8",
            "cargo_test": "passed",
            "wd02_contract": {
                "digest_multibase": True,
                "proof_excluded_from_digest": True,
                "vac_parent_digest": True,
                "vdc_acceptance": True,
                "vdc_chain_verification": True,
                "valid_until_required": True,
            },
            "not_implemented": ["status_resolution", "integrated_trust_task_action_time_evaluator"],
        }
        result = run_action_time.build_result(target_evidence=target)
        self.assertEqual(target, result["target_runtime_evidence"])
        self.assertEqual("PARTIALLY_EVIDENCED", result["runtime_maturity"])
        self.assertIn("integrated Trust Task", result["remaining_gap"])
        self.assertIn("does not establish current consequential authority", result["claim_boundary"])
        self.assertTrue(result["all_expected_outcomes_matched"])


if __name__ == "__main__":
    unittest.main()
