import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CredentialTaskActuationTests(unittest.TestCase):
    def evidence(self):
        cp = subprocess.run([sys.executable, "experiments/dtg-credential-task-actuation/run.py"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        return json.loads(cp.stdout)

    def test_all_issue_vectors_are_present_and_classified(self):
        result = self.evidence()
        vectors = result["vectors"]
        self.assertEqual(len(vectors), 9)
        self.assertEqual({v["id"] for v in vectors}, {"CTA-POS-001", *{f"CTA-NEG-{i:03d}" for i in range(1,9)}})
        allowed = {"supported", "divergent", "not-implemented", "not-observable"}
        self.assertTrue(all(v["classification"] in allowed for v in vectors))

    def test_no_missing_surface_is_promoted_to_supported(self):
        result = self.evidence()
        by_id = {v["id"]: v for v in result["vectors"]}
        self.assertEqual(by_id["CTA-POS-001"]["classification"], "not-implemented")
        self.assertEqual(by_id["CTA-NEG-004"]["classification"], "not-observable")
        self.assertEqual(by_id["CTA-NEG-006"]["effect_count"], "not-observable")
        self.assertEqual(by_id["CTA-NEG-008"]["classification"], "not-implemented")

    def test_evidence_is_raHP_consumable_and_source_pinned(self):
        result = self.evidence()
        self.assertEqual(result["schema"], "interop-actuation-evidence/v1")
        self.assertEqual(set(result["rahp_propositions"]), {"P03","P04","P05","P08","P09"})
        self.assertTrue(all(len(v) == 40 for v in result["source_epoch"].values()))
        self.assertEqual(result["summary"]["divergent"], 0)

if __name__ == "__main__":
    unittest.main()
