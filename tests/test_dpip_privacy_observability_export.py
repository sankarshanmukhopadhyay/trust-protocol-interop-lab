import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "experiments/dtg-protected-access/export_dpip_evidence.py"
spec = importlib.util.spec_from_file_location("export_dpip_evidence", MODULE)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


def capture(classification="fresh", executed=True):
    execution = "executed" if executed else "not-executed"
    surface = {
        "classification": classification,
        "execution": {"context_a": execution, "context_b": execution},
        "correlator_origin": "none" if classification == "fresh" else "target-derived",
        "producer_component": "example/runtime",
        "context_a": "a-value",
        "context_b": "b-value" if classification == "fresh" else "a-value",
    }
    return {
        "evidence_class": "runtime-upstream-observation",
        "experiment": {
            "kind": "unlinkability-pressure-case",
            "expected_join": "must-not-emerge",
            "observed_join": "not-detected" if classification == "fresh" else "detected",
            "join_surfaces": [] if classification == "fresh" else ["policy_endpoint"],
        },
        "provenance": {
            "producer": "trust-protocol-interop-lab",
            "run_id": "run-001",
            "observed_at": "2026-09-09T00:00:00Z",
            "implementation_repository": "example/runtime",
            "implementation_revision": "a" * 40,
            "context_a_run": "run-a",
            "context_b_run": "run-b",
        },
        "context_descriptors": {
            "A": {"verifier": "v-a", "purpose": "p-a", "challenge": "c-a"},
            "B": {"verifier": "v-b", "purpose": "p-b", "challenge": "c-b"},
        },
        "requirements": {
            "ER-STATUS-AB": {
                "observation_summary": "bounded policy discovery A/B observation",
                "surfaces": {
                    "policy_discovery_handle": surface,
                    "policy_endpoint": dict(surface),
                },
            }
        },
    }


class DpipPrivacyObservabilityExportTests(unittest.TestCase):
    def test_fresh_executed_surfaces_support_bounded_privacy_proposition(self):
        result = exporter.export_privacy_observability_result(
            capture(),
            requirement_id="ER-STATUS-AB",
            surface_names=["policy_discovery_handle", "policy_endpoint"],
            experiment_id="track-b-policy-discovery-ab",
        )
        self.assertEqual("dpip-privacy-observability-result/v1", result["schema"])
        self.assertEqual("supported", result["result"])
        self.assertTrue(result["executed"])
        self.assertEqual("not-found", result["correlation"]["signal"])
        self.assertIn("deployment-wide unlinkability", result["unsupported_inference"])

    def test_detected_join_is_not_supported(self):
        result = exporter.export_privacy_observability_result(
            capture(classification="identical"),
            requirement_id="ER-STATUS-AB",
            surface_names=["policy_discovery_handle", "policy_endpoint"],
            experiment_id="track-b-policy-discovery-ab",
        )
        self.assertEqual("not-supported", result["result"])
        self.assertTrue(result["correlation"]["effective_join"])

    def test_non_execution_fails_closed_as_evidence_incomplete(self):
        result = exporter.export_privacy_observability_result(
            capture(executed=False),
            requirement_id="ER-STATUS-AB",
            surface_names=["policy_discovery_handle", "policy_endpoint"],
            experiment_id="track-b-policy-discovery-ab",
        )
        self.assertEqual("evidence-incomplete", result["result"])
        self.assertFalse(result["executed"])
        self.assertEqual("not-tested", result["correlation"]["signal"])


if __name__ == "__main__":
    unittest.main()
