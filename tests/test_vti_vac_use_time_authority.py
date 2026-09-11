import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "experiments/vti-vac-use-time-authority/evaluate.py"
spec = importlib.util.spec_from_file_location("vti_vac_use_time", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VtiVacUseTimeAuthorityTests(unittest.TestCase):
    def base(self):
        return {
            "presenter_from_request_proof": True,
            "exact_action_authorize_before_effect": True,
            "authorized_action_typestate": True,
            "credential_proof_verification": True,
            "room_root_and_scope_binding": True,
            "action_binding_and_non_widening": True,
            "validity_window_checked": True,
            "presenter_binding": True,
            "membership_authority_subject_coherence": True,
            "no_verifier_fails_closed": True,
            "private_without_zk_fails_closed": True,
            "current_status_revocation": False,
            "live_policy_lookup": False,
            "vti_rooms_tests": "passed",
            "vti_rooms_dtg_tests": "passed",
        }

    def test_use_time_authority_is_bounded_not_overclaimed(self):
        result = module.evaluate(self.base(), "8541848176ec9707e24b24f57b09eb9650935a95")
        self.assertEqual("SOURCE_PINNED_USE_TIME_AUTHORITY_EVIDENCE", result["evidence_maturity"])
        self.assertEqual("PARTIALLY_DISCHARGED", result["r001"])
        self.assertIn("revocation", result["remaining_gap"])
        self.assertIn("live policy", result["remaining_gap"])

    def test_missing_core_authority_observation_fails_closed(self):
        observations = self.base()
        observations["presenter_binding"] = False
        with self.assertRaises(ValueError):
            module.evaluate(observations, "8541848176ec9707e24b24f57b09eb9650935a95")


if __name__ == "__main__":
    unittest.main()
