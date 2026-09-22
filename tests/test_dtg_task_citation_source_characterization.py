import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
FIXTURE = (
    ROOT
    / "experiments"
    / "dtg-task-citation-convergence"
    / "openvtc-source-characterization.json"
)


class OpenVtcTaskCitationSourceCharacterizationTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_characterization_is_source_pinned(self):
        target = self.doc["target"]
        self.assertEqual("OpenVTC/verifiable-trust-infrastructure", target["repository"])
        self.assertEqual(40, len(target["revision"]))

    def test_current_implementation_is_not_promoted_to_new_binding_semantics(self):
        observed = self.doc["observed_source_semantics"]
        self.assertEqual(
            "threadId of the Trust Task exchange in which the credential was issued",
            observed["taskContext"]["meaning"],
        )
        self.assertFalse(observed["taskDigestMultibase"]["implemented"])
        self.assertFalse(observed["initiating_document_binding"]["implemented"])
        self.assertEqual(
            "not-implemented",
            self.doc["classification"]["new_initiating_document_plus_digest_path"],
        )

    def test_source_characterization_does_not_claim_runtime_privacy(self):
        self.assertEqual(
            "unresolved",
            self.doc["classification"]["runtime_correlation_result"],
        )
        self.assertIn(
            "source characterization is not runtime evidence",
            self.doc["non_inference"],
        )


if __name__ == "__main__":
    unittest.main()
