import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "experiments/dtg-data-room-runtime/portable_evidence.py"
spec = importlib.util.spec_from_file_location("portable_evidence", MODULE)
portable_evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(portable_evidence)


class PortableEvidenceResultTests(unittest.TestCase):
    def test_preserves_case_propositions_and_non_inference_boundary(self):
        legacy = {
            "schema": "interop-evidence-package/v1",
            "case": "IC-DTG-DATA-ROOM-RUNTIME-001",
            "target": {"repository": "OpenVTC/verifiable-trust-infrastructure", "revision": "a" * 40},
            "evidence_class": "runtime-upstream-observation",
            "propositions": {"P-ROOM-009": {"state": "EVIDENCE_REQUIRED"}},
            "claim_boundary": "Missing evidence remains a residual rather than PASS.",
        }
        result = portable_evidence.build_portable_result(
            legacy,
            producer_revision="b" * 40,
            artifact_sha256="c" * 64,
            proposition_key="rahp-obligation:" + "d" * 20,
            evidence_contract_key="rahp-evidence-contract:" + "e" * 20,
            execution_id="data-room-runtime-123",
            execution_timestamp="2026-09-09T01:23:45Z",
        )
        self.assertEqual("rahp-evidence-producer-result/v1", result["schema"])
        self.assertEqual(legacy["propositions"], result["evidence"]["observations"][0]["propositions"])
        self.assertIn("terminal assurance PASS", result["claim_boundary"]["does_not_support"])
        self.assertEqual("a" * 40, result["freshness"]["valid_against"][0]["revision"])
        self.assertEqual("rahp-obligation:" + "d" * 20, result["obligation"]["proposition_key"])
        self.assertEqual("rahp-evidence-contract:" + "e" * 20, result["obligation"]["evidence_contract_key"])
        self.assertEqual("data-room-runtime-123", result["execution"]["id"])
        self.assertEqual("2026-09-09T01:23:45Z", result["execution"]["timestamp"])


if __name__ == "__main__":
    unittest.main()
