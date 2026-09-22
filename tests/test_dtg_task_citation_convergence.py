import importlib.util
import unittest
from pathlib import Path

MODULE = (
    Path(__file__).parents[1]
    / "experiments"
    / "dtg-task-citation-convergence"
    / "evaluate.py"
)
spec = importlib.util.spec_from_file_location("task_citation_convergence", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class TaskCitationConvergenceTests(unittest.TestCase):
    def test_valid_credential_without_outcome_evidence_does_not_prove_completion(self):
        result = module.evaluate_vector(
            {
                "id": "TCC-NEG-001",
                "credential_valid": True,
                "task_context_matches": True,
                "task_digest_matches": True,
                "completion_required": True,
                "outcome_evidence_present": False,
                "outcome_evidence_valid": False,
                "action_authorized": True,
                "visible_citation": True,
                "same_citation_across_contexts": True,
                "expected": {
                    "credential_validity": "confirmed",
                    "citation_binding": "confirmed",
                    "completion": "contradicted",
                    "authorization": "confirmed",
                    "correlation": "confirmed",
                },
            }
        )
        self.assertEqual("supported", result["classification"])

    def test_reused_thread_equivalent_cannot_substitute_for_exact_initiating_document(self):
        result = module.evaluate_vector(
            {
                "id": "TCC-NEG-002",
                "credential_valid": True,
                "task_context_matches": False,
                "task_digest_matches": False,
                "completion_required": True,
                "outcome_evidence_present": True,
                "outcome_evidence_valid": True,
                "action_authorized": True,
                "visible_citation": True,
                "same_citation_across_contexts": False,
                "expected": {
                    "citation_binding": "contradicted",
                    "completion": "contradicted",
                },
                "reason": "same/reused thread-level context is insufficient",
            }
        )
        self.assertEqual("supported", result["classification"])

    def test_correct_context_with_wrong_digest_fails_exact_binding(self):
        result = module.evaluate_vector(
            {
                "id": "TCC-NEG-003",
                "credential_valid": True,
                "task_context_matches": True,
                "task_digest_matches": False,
                "completion_required": True,
                "outcome_evidence_present": True,
                "outcome_evidence_valid": True,
                "action_authorized": True,
                "visible_citation": False,
                "same_citation_across_contexts": False,
                "expected": {
                    "citation_binding": "contradicted",
                    "completion": "contradicted",
                },
            }
        )
        self.assertEqual("supported", result["classification"])

    def test_valid_completion_evidence_does_not_create_action_authority(self):
        result = module.evaluate_vector(
            {
                "id": "TCC-NEG-004",
                "credential_valid": True,
                "task_context_matches": True,
                "task_digest_matches": True,
                "completion_required": True,
                "outcome_evidence_present": True,
                "outcome_evidence_valid": True,
                "action_authorized": False,
                "visible_citation": False,
                "same_citation_across_contexts": False,
                "expected": {
                    "completion": "confirmed",
                    "authorization": "contradicted",
                },
            }
        )
        self.assertEqual("supported", result["classification"])

    def test_visible_stable_citation_is_recorded_as_correlation_surface(self):
        result = module.evaluate_vector(
            {
                "id": "TCC-PRIV-001",
                "credential_valid": True,
                "task_context_matches": True,
                "task_digest_matches": True,
                "completion_required": True,
                "outcome_evidence_present": True,
                "outcome_evidence_valid": True,
                "action_authorized": True,
                "visible_citation": True,
                "same_citation_across_contexts": True,
                "expected": {"correlation": "confirmed"},
            }
        )
        self.assertEqual("supported", result["classification"])
        self.assertEqual("confirmed", result["correlation"])

    def test_absent_target_runtime_is_not_implemented_not_pass(self):
        result = module.evaluate_vector(
            {
                "id": "TCC-RUNTIME-001",
                "surface": "target-runtime",
                "runtime_available": False,
            }
        )
        self.assertEqual("not-implemented", result["classification"])
        self.assertEqual("unresolved", result["completion"])

    def test_case_preserves_authority_state_and_summary(self):
        package = module.evaluate_case(
            {
                "case": "IC-DTG-TASK-CITATION-CONVERGENCE-001",
                "vectors": [
                    {
                        "id": "TCC-POS-001",
                        "credential_valid": True,
                        "task_context_matches": True,
                        "task_digest_matches": True,
                        "completion_required": True,
                        "outcome_evidence_present": True,
                        "outcome_evidence_valid": True,
                        "action_authorized": True,
                        "visible_citation": False,
                        "same_citation_across_contexts": False,
                        "expected": {
                            "completion": "confirmed",
                            "authorization": "confirmed",
                        },
                    },
                    {
                        "id": "TCC-RUNTIME-001",
                        "surface": "target-runtime",
                        "runtime_available": False,
                    },
                ],
            }
        )
        self.assertEqual("merged", package["authority_state"]["trust_tasks_17"])
        self.assertEqual("open-proposal", package["authority_state"]["credential_56"])
        self.assertEqual(1, package["summary"]["supported"])
        self.assertEqual(1, package["summary"]["not-implemented"])
        self.assertIn("fixture support != target-runtime conformance", package["non_inference"])


if __name__ == "__main__":
    unittest.main()
