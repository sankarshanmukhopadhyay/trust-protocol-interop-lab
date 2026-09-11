import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "experiments/vti-credential-replay-convergence/evaluate.py"
spec = importlib.util.spec_from_file_location("vti_replay", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReplayConvergenceTests(unittest.TestCase):
    def observations(self):
        return {
            "issue_authority_keyed": True,
            "signed_idempotency_key": True,
            "actor_key_payload_binding": True,
            "conflict_fails_closed": True,
            "completed_response_replayed": True,
            "failed_outcome_releases_claim": True,
            "dispatcher_claims_before_dispatch": True,
            "dispatcher_records_after_dispatch": True,
            "target_package_tests": "passed",
        }

    def test_bounded_replay_evidence(self):
        result = module.evaluate(self.observations(), "8541848176ec9707e24b24f57b09eb9650935a95")
        self.assertEqual("SOURCE_PINNED_REPLAY_CONVERGENCE_EVIDENCE", result["evidence_maturity"])
        self.assertEqual("PARTIALLY_DISCHARGED", result["r002"])
        self.assertIn("does not establish current downstream authority", result["claim_boundary"])

    def test_missing_guard_fails_closed(self):
        obs = self.observations()
        obs["conflict_fails_closed"] = False
        with self.assertRaises(ValueError):
            module.evaluate(obs, "8541848176ec9707e24b24f57b09eb9650935a95")


if __name__ == "__main__":
    unittest.main()
