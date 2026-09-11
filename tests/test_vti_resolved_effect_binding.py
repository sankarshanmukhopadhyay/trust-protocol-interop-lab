import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "experiments/vti-resolved-effect-binding/evaluate.py"
spec = importlib.util.spec_from_file_location("vti_resolved_effect", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VtiResolvedEffectBindingTests(unittest.TestCase):
    def test_source_establishes_distinct_resolved_effect_branches_without_overclaim(self):
        observations = {
            "vault_write_gate": True,
            "context_scope_gate": True,
            "version_gate": True,
            "force_hard_delete": True,
            "soft_delete_grace": True,
            "audit_declared": True,
            "target_package_tests": "passed",
            "runtime_branch_test": False,
            "approval_surface_observed": False,
        }
        result = module.evaluate(observations, "8541848176ec9707e24b24f57b09eb9650935a95")
        self.assertEqual("SOURCE_PINNED_EFFECT_BINDING_EVIDENCE", result["evidence_maturity"])
        self.assertEqual("ESTABLISHED_IN_SOURCE", result["resolved_effect"])
        self.assertEqual("PARTIALLY_DISCHARGED", result["r001"])
        self.assertEqual("PARTIALLY_DISCHARGED", result["r002"])
        self.assertEqual("EVIDENCE_REQUIRED", result["f004_retained_agency"])
        self.assertIn("Missing runtime evidence remains non-PASS", result["claim_boundary"])

    def test_missing_force_branch_fails_closed(self):
        observations = {
            "vault_write_gate": True,
            "context_scope_gate": True,
            "version_gate": True,
            "force_hard_delete": False,
            "soft_delete_grace": True,
            "audit_declared": True,
            "target_package_tests": "passed",
            "runtime_branch_test": False,
            "approval_surface_observed": False,
        }
        with self.assertRaises(ValueError):
            module.evaluate(observations, "8541848176ec9707e24b24f57b09eb9650935a95")


if __name__ == "__main__":
    unittest.main()
